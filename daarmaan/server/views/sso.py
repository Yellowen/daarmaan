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

import json
import urllib
import hashlib
from urlparse import urlparse

from django.conf.urls import patterns, include, url
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseForbidden)
from django.conf import settings
from vakhshour.base import Node

from daarmaan.server.models import Service
from daarmaan.utils import DefaultValidation


class DaarmaanServer(object):
    """
    Daarmaan SSO service server class. This class take care of SSO activities.
    """

    node = Node(**settings.VAKHSHOUR)

    @property
    def urls(self):
        """
        Url dispatcher property.
        """
        urlpatterns = patterns('',
                url(r'^authenticate/$', self.authenticate,
                    name="remote-auth"),
                url(r'^verification/$', self.verify,
                    name="remote-auth"),
                url(r"^logout/$", self.logout,
                    name="logout"),
                )
        return urlpatterns

    def authenticate(self, request):
        """
        Check the request for authenticated user. If user is not authenticated
        then redirect user to login view.
        """

        next_url = request.GET.get("next", None)

        service = self._get_service(request)

        if not service:
            return HttpResponseForbidden("Invalid service")

        validator = DefaultValidation(service.key)

        next_url = urlparse(urllib.unquote(next_url).decode("utf8"))

        # Does user authenticated before?
        if request.user.is_authenticated():

            # If user is authenticated in Daarmaan then a ticket
            # (user session ID) will send back to service
            ticket = request.session.session_key

            params = {'ticket': ticket,
                      "hash": validator.sign(ticket)}

            next_url = "%s?%s" % (next_url.geturl(), urllib.urlencode(params))

        else:
            # If user is not authenticated simple ack answer will return
            params = {"ack": ""}
            next_url = "%s?%s" % (next_url.geturl(), urllib.urlencode(params))

        return HttpResponseRedirect(next_url)

    def verify(self, request):
        """
        verify the user token that friend service sent.
        """

        hash_ = request.GET.get("hash", None)
        token = request.GET.get("token", None)
        service = self._get_service(request)

        if not hash_ or not token or not service:
            return HttpResponseForbidden()

        validator = DefaultValidation(service.key)


        if not validator.is_valid(token, hash_):
            return HttpResponseForbidden()

        try:
            session = Session.objects.get(session_key=token)

        except Session.DoesNotExist:
            pass

        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)

        if user.is_authenticated():
            # TODO: Add more details in this dict
            a = {
                "id": user.id,
                "username": user.username,
                 "first_name": user.first_name,
                 "last_name": user.last_name,
                 "email": user.email,
                 "id": user.pk,
                 "is_staff": user.is_staff,
                 "is_active": user.is_active,
                 }
            m = True
        else:
            a = {"username": ""}
            m = False

        # TODO: rethink this terminology
        result = {"data": a}
        if m:
            result.update({"hash": validator.sign(user.username)})
        else:
            result.update({"hash": ""})

        return HttpResponse(json.dumps(result))

    def logout(self, request):
        """
        Log the user out and send the logout event.
        """
        next_url = request.GET.get("next", None)
        service = request.GET.get("service", None)

        if request.user.is_authenticated():
            logout(request)

            # Send the logout event
            self.node.send_event(name="logout", sender="daarmaan",
                                 ticket=request.session.session_key)

        if not next_url:
            next_url = request.META.get("HTTP_REFERER", None)

        if not next_url:
            next_url = "/"

        return HttpResponseRedirect(next_url)

    def _get_service(self, request):
        """
        Extract the service object from request.
        """
        service = request.GET.get("service", None)

        if not service:
            return None

        try:
            service = Service.objects.get(name=service,
                                          active=True)
        except Service.DoesNotExist:
            return None

        return service


daarmaan_service = DaarmaanServer()
