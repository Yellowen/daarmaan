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

# This file is a part of Daarmaan Global authentication service.
import datetime
import urllib

from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.signals import user_logged_in

from daarmaan.client.models import SSOSession


class HttpResponseRedirectAuth(HttpResponsePermanentRedirect):
    pass


class DaarmaanAuthMiddleware(object):
    """
    This middleware authenticate user against Daarmaan.
    """

    def process_request(self, request):
        # Stay with redirection only

        # If user was authenticated we don't need to check for SSO status
        if request.user.is_authenticated():
            return None

        # If redirected key exists in user session it means that
        # we redirect the user to same page again to get rid of
        # SSO GET parameters
        if "redirected" in request.session:
                del request.session["redirected"]
                return None

        ticket = request.GET.get("ticket", None)
        ack = request.GET.get("ack", None)

        # If ack key exists in request.GET user was not authenticated
        # in SSO service
        if ack:
            path = self._striped_path(request)
            request.session["redirected"] = request.path.split("?")[0]
            return HttpResponseRedirect(path)

        # Existance of ticket parameter means that user authenticated
        # in SSO system
        if ticket:
            hash_ = request.GET.get("hash", "")

            # Use the SSO authentication backend to authenticate the user
            # and token
            user = authenticate(request=request, token=ticket, hash_=hash_)

            # If user was valid log him/her in
            if user:
                self.login(request, user, ticket)

            path = self._striped_path(request)

            request.session["redirected"] = request.path.split("?")[0]
            return HttpResponseRedirect(path)

        # Send user to SSO service
        return self.redirect(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_response(self, request, response):
        return response

    def _gen_link(self, domain, **kwargs):
        return "%s?%s" % (domain, urllib.urlencode(kwargs))

    def _strip_ack(self, request):
        """
        Strip SSO GET params from request.
        """
        a = request.GET.copy()
        if "ack" in a:
            del a["ack"]
        if "ticket" in a:
            del a["ticket"]
        if "hash" in a:
            del a["hash"]
        return a

    def _striped_path(self, request):
        a = self._strip_ack(request)
        path = request.path
        if a:
            path = "%s?%s" % (path, urllib.urlencode(a))
        return path

    def _strip_request(self, request):
        a = self._strip_ack(request)
        setattr(request, "GET", a)
        return request

    def redirect(self, request):
        """
        Redirect user to SSO service.
        """
        if "redirect" in request.session:
            del request.session["redirect"]

        login_url = settings.DAARMAAN_LOGIN
        service_name = settings.SERVICE_NAME

        # Get the current location and escape it
        next_url = urllib.quote_plus(request.build_absolute_uri())

        url = self._gen_link(login_url, next=next_url,
                             service=service_name)

        return HttpResponseRedirectAuth(url)

    def login(self, request, user, ticket):
        """
        Log the user in and save the recieved ticket for later
        use.
        """
        login(request, user)
        sso_session = SSOSession(session=request.session.session_key,
                                 sso_session=ticket,
                                 user=user)
        sso_session.save()
