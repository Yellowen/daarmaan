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
import pickle
import urllib
import hashlib
from urlparse import urlparse

from django.conf.urls import patterns, include, url
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseForbidden)
from gauth.models import Service


class DaarmaanServer(object):
    """
    Daarmaan SSO service server class.
    """

    @property
    def urls(self):
        urlpatterns = patterns('',
                url(r'^authenticate/$', self.authenticate,
                    name="remote-auth"),
                url(r'^verification/$', self.verify,
                    name="remote-auth"),
                #url(r"^login/$", self.login_view,
                #    name="login"),
                )
        return urlpatterns

    def authenticate(self, request):
        """
        Check the request for authenticated user.
        """

        next_url = request.GET.get("next", None)

        service = self._get_service(request)

        if not service:
            return HttpResponseForbidden("Invalid service")

        next_url = urlparse(urllib.unquote(next_url).decode("utf8"))

        # Does user authenticated before?
        if request.user.is_authenticated():
            ticket = request.session.session_key

            params = {'ticket': ticket,
                      "hash": self._checksum(service, ticket)}

            next_url = "%s?%s" % (next_url.geturl(), urllib.urlencode(params))

        else:
            print "asdasd ", request.session.__dict__
            params = {"ack": request.session.session_key}
            next_url = "%s?%s" % (next_url.geturl(), urllib.urlencode(params))

        return HttpResponseRedirect(next_url)

    def verify(self, request):
        """
        verify the user token that friend server sent.
        """

        hash_ = request.GET.get("hash", None)
        token = request.GET.get("token", None)
        service = self._get_service(request)

        if not hash_ or not token or not service:
            return HttpResponseForbidden()

        if hash_ != self._checksum(service, token):
            return HttpResponseForbidden()

        try:
            session = Session.objects.get(session_key=token)
        except Session.DoesNotExist:
            pass

        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)

        #if user.is_authenticated():
            # TODO: Add more details in this dict
            ## a = {"username": user.username,
            ##      "first_name": user.first_name,
            ##      "last_name": user.last_name,
            ##      "email": user.email,
            ##      "id": user.pk,
            ##      "is_stuff": user.is_stuff,
            ##      "is_active": user.is_active,
            ##      }
            #a = pickle.dumps(user, 2)
            #m.update(user + service.key)
        #else:
        #a = {"username": ""}
        #    m = None
        a = pickle.dumps(user)

        # TODO: rethink this terminology
        result = {"data": a}
        #if m:
        result.update({"hash": self._checksum(service, a)})
        #else:
        #    result.update({"hash": ""})

        return HttpResponse(json.dumps(result))

    ## def logout(self, request):

    ##     next_url = request.GET.get("next", None)
    ##     service = request.GET.get("service", None)
    ##     if request.user.is_authenticated():
    ##         logout(request)

    ##     if not next_url:
    ##         next_url = request.META.get("HTTP_REFERER", None)

    ##     if not next_url:
    ##         next_url = "/"

    ##     return HttpResponseRedirect(next_url)

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

    def _checksum(self, service, value):
        """
        Return the checksum of value plus service key.
        """
        m = hashlib.sha1()
        m.update(value + service.key)
        return m.hexdigest()


daarmaan_service = DaarmaanServer()
