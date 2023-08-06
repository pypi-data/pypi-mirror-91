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


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from allauth.account.models import EmailAddress

from django_mailman3.forms import UserProfileForm
from django_mailman3.lib.mailman import get_mailman_user
from django_mailman3.models import Profile


@login_required
def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Create the profile if it does not exist. There's a signal receiver
        # that creates it for new users, but this app may be added to an
        # existing Django project with existing users.
        profile = Profile.objects.create(user=request.user)
    mm_user = get_mailman_user(request.user)
    initial_data = {
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "timezone": profile.timezone,
        }

    if request.method == 'POST':
        form = UserProfileForm(request.POST, initial=initial_data)
        if form.is_valid():
            if form.has_changed():
                request.user.username = form.cleaned_data["username"]
                request.user.first_name = form.cleaned_data["first_name"]
                request.user.last_name = form.cleaned_data["last_name"]
                profile.timezone = form.cleaned_data["timezone"]
                request.user.save()
                profile.save()
                # Now update the display name in Mailman
                if mm_user is not None:
                    mm_user.display_name = "%s %s" % (
                            request.user.first_name, request.user.last_name)
                    mm_user.save()
                messages.success(
                    request, _("The profile was successfully updated."))
            else:
                messages.success(request, _("No change detected."))
            return redirect(reverse('mm_user_profile'))
    else:
        form = UserProfileForm(initial=initial_data)

    # Emails
    other_addresses = EmailAddress.objects.filter(
        user=request.user).exclude(
        email=request.user.email).order_by("email").values_list(
        'email', flat=True)

    # Extract the gravatar_url used by django_gravatar2.  The site
    # administrator could alternatively set this to http://cdn.libravatar.org/
    gravatar_url = getattr(settings, 'GRAVATAR_URL', 'http://www.gravatar.com')
    gravatar_shortname = '.'.join(gravatar_url.split('.')[-2:]).strip('/')

    context = {
        'user_profile': profile,
        'form': form,
        'other_addresses': other_addresses,
        'gravatar_url': gravatar_url,
        'gravatar_shortname': gravatar_shortname,
    }
    return render(request, "django_mailman3/profile/profile.html", context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        mm_user = get_mailman_user(request.user)
        if mm_user:
            mm_user.delete()
        request.user.delete()
        messages.success(request, _("Successfully deleted account"))
        return HttpResponseRedirect('/')
    return render(request, 'django_mailman3/profile/delete_profile.html',
                  {'delete_page': True})
