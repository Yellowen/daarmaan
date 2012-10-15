# -----------------------------------------------------------------------------
#    Daarmaan - Single Sign On Service for Yellowen
#    Copyright (C) 2012 Yellowen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from django.conf.urls import patterns, url
from django.template import RequestContext
from django.shortcuts import render_to_response as rr
from django.http import HttpResponseRedirect, Http404

from daarmaan.server.models import BasicProfile


class ProfileActions(object):
    """
    Profile related action like:
        Review user profiles
        Edit profile
        etc
    """

    view_profile_template = "view_profile.html"
    edit_profile_template = "edit_profile.html"

    @property
    def urls(self):
        """
        Profile Page url patterns.
        """
        urlpatterns = patterns(
            '',
            url(r"^$", self.index,
                name="profile-home"),
            url(r"^edit/$", self.edit,
                name="edit-profile"),
            )
        return urlpatterns

    def index(self, request):
        """
        Index view.
        """
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')

        if request.method == "POST":
            raise Http404()
        else:
            try:
                profile = BasicProfile.objects.get(
                    user=request.user)

            except BasicProfile.DoesNotExist:
                profile = BasicProfile(user=request.user)
                profile.save()

            return rr(self.view_profile_template,
                      {"user": request.user,
                       "profile": profile},
                      context_instance=RequestContext(request))

    def edit(self, request):
        return HttpResponseRedirect('/')


profile = ProfileActions()
