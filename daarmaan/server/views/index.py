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

from django.shortcuts import render_to_response as rr
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseForbidden)
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url

from daarmaan.server.views.sso import daarmaan_service
from daarmaan.server.forms import PreRegistrationForm
from daarmaan.server.models import Profile, Service, VerificationCode


class IndexPage(object):
    """
    Daarmaan index page class.
    """
    template = "index.html"

    @property
    def urls(self):
        """
        First Page url patterns.
        """
        urlpatterns = patterns(
            '',
            url(r"^$", self.index,
                name="home"),
            url(r"^verificate/$", self.verificate,
                name="verificate"),

            )
        return urlpatterns

    def index(self, request):
        """
        Index view.
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard-index'))

        if request.method == "POST":
            return self.on_post(request)
        else:
            return self.on_get(request)

    def on_get(self, request):
        """
        This view handles GET requests.
        """
        form = PreRegistrationForm()
        next_url = request.GET.get("next", "")
        return rr(self.template,
                  {"regform": form,
                   "next": next_url},
                  context_instance=RequestContext(request))

    def on_post(self, request):
        """
        This view handles POST requests.
        """

        if request.POST["form"] == "login":
            return self.login(request)
        else:
            return self.pre_register(request)

    def login(self, request):
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get("remember_me", False)
        next_url = request.POST.get("next", None)
        form = PreRegistrationForm()

        user = authenticate(username=username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                self._setup_session(request)

                if next_url:
                    return HttpResponseRedirect(next_url)

                return redirect(reverse(
                    "dashboard-index",
                    args=[]))
            else:
                return rr(self.template,
                          {"regform": form,
                           "msgclass": "error",
                           "next": next_url,
                           "msg": _("Your account is disabled.")},
                          context_instance=RequestContext(request))

        else:
            return rr(self.template,
                      {"regform": form,
                       "msgclass": "error",
                       "next": next_url,
                       "msg": _("Username or Password is invalid.")},
                      context_instance=RequestContext(request))

    def pre_register(self, request):
        """
        Handle the registeration request.
        """
        from django.contrib.auth.models import User
        from django.db import IntegrityError

        form = PreRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]

            # Check for exists email
            emails_count = User.objects.filter(email=email).count()
            if emails_count:
                failed = True
                msg = _("This email has been registered before.")
                klass = "error"
            else:
                try:
                    user = User(username=username,
                                email=email)
                    user.active = False
                    user.save()

                    verif_code = VerificationCode.generate(user)
                    print ">>>>> ", verif_code
                    verification_link = reverse('verificate', args=[])

                    print ">>>>> ", verif_code, verification_link
                    msg = _("A verfication mail has been sent to your e-mail address.")
                    klass = "info"
                except IntegrityError:
                    # In case of exists username
                    msg = _("User already exists.")
                    klass = "error"

        return rr(self.template,
                  {"regform": form,
                   "msgclass": klass,
                   "msg": msg},
                  context_instance=RequestContext(request))

    def _setup_session(self, request):
        """
        Insert all needed values into user session.
        """
        return
        services = request.user.get_profile().services.all()
        services_id = [i.id for i in services]
        request.session["services"] = services_id

    def verificate(self, request):
        return HttpResponse()

index_page = IndexPage()
