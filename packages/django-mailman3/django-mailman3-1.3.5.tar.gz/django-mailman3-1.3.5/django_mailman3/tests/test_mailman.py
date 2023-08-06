# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2019 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
#
# Django-Mailman is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Django-Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aurelien Bompard <abompard@fedoraproject.org>
#

from unittest.mock import Mock, call, patch
from urllib.error import HTTPError

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import IntegrityError

from allauth.account.models import EmailAddress

from django_mailman3.lib import mailman
from django_mailman3.tests.utils import (
    FakeMMAddress, FakeMMAddressList, FakeMMList, FakeMMMember, TestCase)


class GetMailmanUserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testPass')
        self.mm_user = Mock()
        self.mm_user.user_id = "dummy"
        self.mailman_client.get_user.side_effect = lambda e: self.mm_user

    def test_get_user(self):
        mm_user = mailman.get_mailman_user(self.user)
        self.assertIs(mm_user, self.mm_user)

    @patch('django_mailman3.lib.mailman.get_mailman_user',
           return_value=None)
    def test_get_nonexistent_user(self, mock_method):
        # Test create user fails and get_mailman_user returns None.
        mm_user = mailman.get_mailman_user(self.mm_user)
        self.assertIsNone(mm_user)
        mock_method.assert_called_with(self.mm_user)

    def test_create_user(self):
        self.mailman_client.get_user.side_effect = \
            HTTPError(None, 404, None, None, None)
        new_mm_user = Mock()
        new_mm_user.user_id = "dummy2"
        self.mailman_client.create_user.side_effect = lambda e, n: new_mm_user
        mm_user = mailman.get_mailman_user(self.user)
        self.assertEqual(
            self.mailman_client.create_user.call_args_list,
            [call(self.user.email, self.user.get_full_name())])
        self.assertIs(mm_user, new_mm_user)

    def test_connection_failed(self):
        self.mailman_client.get_user.side_effect = \
            HTTPError(None, 500, None, None, None)
        with patch('django_mailman3.lib.mailman.logger') as mock_logging:
            mm_user = mailman.get_mailman_user(self.user)
        # Make sure that the returned user is None.
        self.assertIsNone(mm_user)
        # Make sure the failure is logged.
        mock_logging.warning.assert_called()

    def test_get_user_id(self):
        mm_user_id = mailman.get_mailman_user_id(self.user)
        self.assertEqual(mm_user_id, "dummy")

    def test_bad_cached_user_id(self):
        # Test that we lookup a user via email if the cached user_id is invalid
        # and doesn't return a valid user.
        new_mm_user = Mock()
        new_mm_user.user_id = "dummy3"

        def side_effect(user_id):
            if user_id == '4':
                raise HTTPError(
                    url='', code=404, msg='No user with id 4',
                    hdrs=None, fp=None)
            elif user_id == 'test@example.com':
                return new_mm_user
            return None

        self.mailman_client.get_user.side_effect = side_effect
        # Now, also set integer user_id 4 in the cache.
        cache.set("User:{0}:mailman_user_id".format(self.user.id), '4', None)

        mm_user = mailman.get_mailman_user(self.user)
        self.assertIsNotNone(mm_user)
        self.assertEqual(mm_user, new_mm_user)

        expected = [call('4'), call('test@example.com')]
        self.mailman_client.get_user.call_args_list == expected


class AddUserToMailmanTestCase(TestCase):

    def setUp(self):
        self.ml = FakeMMList("list@example.com")
        self.mailman_client.get_list.side_effect = lambda n: self.ml
        self.ml.get_member = Mock()
        self.ml.subscribe = Mock()
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testPass')
        self.mm_user = Mock()
        self.mm_user.user_id = "dummy"
        self.mm_user.addresses = []
        self.mailman_client.get_user.side_effect = lambda e: self.mm_user
        self.mm_addresses = {}

    def _get_or_add_address(self, email, **kw):
        try:
            mm_addr = self.mm_addresses[email]
        except KeyError:
            mm_addr = Mock()
            mm_addr.email = email
            mm_addr.verified_on = None
            self.mm_addresses[email] = mm_addr
        return mm_addr

    def test_primary_address_unverified(self):
        self.mailman_client.get_address.side_effect = self._get_or_add_address
        self.mm_user.addresses = ["test@example.com"]
        mailman.add_address_to_mailman_user(self.user, "test@example.com")
        self.mm_addresses['test@example.com'].verify.assert_called_with()
        self.assertFalse(self.mm_user.add_address.called)

    def test_addresses_verified(self):
        self.mm_user.add_address.side_effect = self._get_or_add_address
        mailman.add_address_to_mailman_user(self.user, "secondary@example.com")
        self.mm_user.add_address.assert_called_with(
            "secondary@example.com", absorb_existing=True)
        self.mm_addresses['secondary@example.com'].verify.assert_called_with()

    def test_existing_address_but_not_verified(self):
        # The secondary address exists but is not verified
        self.mailman_client.get_address.side_effect = self._get_or_add_address
        secondary_address = Mock()
        secondary_address.email = "secondary@example.com"
        secondary_address.verified_on = None
        secondary_address.__str__ = lambda self: self.email
        self.mm_user.addresses.append(secondary_address)
        self.mm_addresses["secondary@example.com"] = secondary_address
        mailman.add_address_to_mailman_user(self.user, "secondary@example.com")
        # The secondary address must only have been verified.
        self.assertFalse(self.mm_user.add_address.called)
        secondary_address.verify.assert_called_with()

    @patch('django_mailman3.lib.mailman.logger')
    def test_add_new_address(self, mock_log):
        secondary_address = Mock()
        secondary_address.email = "secondary@example.com"
        with patch('django_mailman3.lib.mailman.get_mailman_user',
                   return_value=None):
            # If the user does not exist, function return and logs the result.
            mailman.add_address_to_mailman_user(self.user, secondary_address)
            mock_log.info.assert_called()


class SyncEmailAddressesTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testPass')
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        self.mm_user = Mock()
        self.mm_user.user_id = "dummy"
        self.mm_user.addresses = FakeMMAddressList()
        self.mailman_client.get_user.side_effect = lambda e: self.mm_user

    def test_sync_django(self):
        # Addresses in Django are pushed to Mailman, verified bits are synced.
        EmailAddress.objects.create(
            user=self.user, email='another@example.com', verified=True)
        not_verified = FakeMMAddress('another@example.com', verified=False)
        self.mm_user.addresses.append(not_verified)
        mailman.sync_email_addresses(self.user)
        # The missing address must have been added
        self.assertEqual(
            self.mm_user.add_address.call_args_list,
            [call('test@example.com', absorb_existing=True)])
        # The unverified address must have been set verified
        self.assertTrue(not_verified.verified)

    def test_sync_mailman(self):
        # Addresses in Mailman are pushed to Django, verified bits are synced.
        self.mm_user.addresses.extend([
            FakeMMAddress('another@example.com', verified=True),
            FakeMMAddress('not-verified@example.com', verified=False),
            FakeMMAddress('yet-another@example.com', verified=True),
            ])
        EmailAddress.objects.create(
            user=self.user, email='yet-another@example.com', verified=False)
        mailman.sync_email_addresses(self.user)
        self.assertEqual(
            list(EmailAddress.objects.filter(
                 user=self.user, verified=True).order_by("email").values_list(
                 "email", flat=True)),
            ['another@example.com', self.user.email,
             'yet-another@example.com'])

    def test_user_conflict(self):
        # A user with two email addresses in Mailman is split in two Django
        # users.
        user2 = User.objects.create_user(
            'testuser2', 'another@example.com', 'testPass')
        EmailAddress.objects.create(
            user=user2, email=user2.email, verified=True)
        self.mm_user.addresses.extend([
            FakeMMAddress('test@example.com', verified=True),
            FakeMMAddress('another@example.com', verified=True),
            ])
        try:
            mailman.sync_email_addresses(self.user)
        except IntegrityError as e:
            self.fail(e)
        self.assertEqual(
            list(EmailAddress.objects.filter(
                user=self.user).values_list("email", flat=True)),
            [self.user.email])
        self.assertEqual(
            list(EmailAddress.objects.filter(
                user=user2).values_list("email", flat=True)),
            [user2.email])


class GetSubscriptionsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testPass')
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        self.mm_user = Mock()
        self.mm_user.user_id = "dummy"
        self.mailman_client.get_user.side_effect = lambda e: self.mm_user

    def test_get_subscriptions(self):
        fake_member = FakeMMMember("list.example.com", "test@example.com")
        self.mm_user.subscriptions = [fake_member]
        self.assertEqual(
            mailman.get_subscriptions(self.user),
            {"list.example.com": "test@example.com"})

    def test_get_subscriptions_no_user(self):
        with patch('django_mailman3.lib.mailman.get_mailman_user') as gmu:
            gmu.return_value = None
            self.assertEqual(mailman.get_subscriptions(self.user), {})

    def test_get_subscriptions_nonmember(self):
        fake_member = FakeMMMember(
            "list.example.com", "test@example.com", role="nonmember")
        self.mm_user.subscriptions = [fake_member]
        self.assertEqual(mailman.get_subscriptions(self.user), {})


class UpdatePreferredAddressTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testPass')
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        self.mm_user = Mock()
        self.mm_user.user_id = "dummy"
        self.mm_user.addresses = FakeMMAddressList()
        self.mailman_client.get_user.side_effect = lambda e: self.mm_user

    def test_update_preferred_address_updates_mailman(self):
        """Updating preferred address in Django updates Core."""
        self.mm_user.addresses.extend([
            FakeMMAddress('another@example.com', verified=False),
            FakeMMAddress('verified@example.com', verified=True),
            ])
        email2 = EmailAddress.objects.create(
            user=self.user, email='another@example.com', verified=False)
        email2.set_as_primary()
        mailman.update_preferred_address(self.user, email2)
        # A non-verified address should never set the preferred address.
        self.assertNotEqual(
            self.mm_user.preferred_address, 'another@example.com')
        email3 = EmailAddress.objects.create(
            user=self.user, email='verified@example.com', verified=True)
        email3.set_as_primary()
        mailman.update_preferred_address(self.user, email3)
        self.assertEqual(
            self.mm_user.preferred_address, 'verified@example.com')

    def test_update_preferred_address_adds_address(self):
        """Setting a preferred address which isn't already created in Core."""
        # Test that we can set an address which isn't already associated with
        # the user in Mailman Core.
        email4 = EmailAddress.objects.create(
            user=self.user, email='not-added@example.com', verified=True)
        email4.set_as_primary()
        mailman.update_preferred_address(self.user, email4)
        self.assertEqual(
            self.mm_user.preferred_address, 'not-added@example.com')
        self.mm_user.add_address.assert_called_once_with(
            'not-added@example.com', absorb_existing=True)
