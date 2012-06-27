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

from gauth.forms import PreRegistrationForm
from gauth.models import Profile, Service


@login_required
def dashboard(request):
    return HttpResponse()


@login_required
def setup_session(request):
    """
    Insert all needed values into user session.
    """
    return
    services = request.user.get_profile().services.all()
    services_id = [i.id for i in services]
    request.session["services"] = services_id


def login_view(request):
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
            setup_session(request)

            if next_url:
                return HttpResponseRedirect("/")

            return redirect(reverse("gauth.views.general.dashboard", args=[]))
        else:
            return rr("index.html", {"regform": form,
                                     "msgclass": "error",
                                     "next": next_url,
                                     "msg": _("Your account is disabled.")},
                          context_instance=RequestContext(request))

    else:
        return rr("index.html", {"regform": form,
                                 "msgclass": "error",
                                 "next": next_url,
                                 "msg": _("Username or Password is invalid.")},
                  context_instance=RequestContext(request))


def pre_register(request):
    return HttpResponse()


def index(request):
    """
    Main page.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect("/my/")

    if request.method == "POST":
        if request.POST["form"] == "login":
            return login_view(request)
        else:
            return pre_register(request)
    else:
        form = PreRegistrationForm()
        next_url = request.GET.get("next", "")
        return rr("index.html", {"regform": form,
                                 "next": next_url},
                  context_instance=RequestContext(request))


def remote_auth(request):
    """
    Check the request for authenticated user.
    """
    import urllib
    import hashlib
    from urlparse import urlparse

    next_url = request.GET.get("next", None)
    service_name = request.GET.get("service", None)

    service = get_object_or_404(Service, name=service_name, active=True)

    next_url = urlparse(urllib.unquote(next_url).decode("utf8"))

    # Does user authenticated before?
    if request.user.is_authenticated():
        ticket = request.session.session_key

        m = hashlib.sha1()
        m.update(ticket + service.key)
        params = {'ticket': ticket,
                  "hash": m.hexdigest()}

        next_url = "%s?%s" % (next_url.geturl(), urllib.urlencode(params))
        return HttpResponseRedirect(next_url)

    else:
        params = {"ack": request.session.session_key}
        next_url = "%s?%s" % (next_url.geturl(), urllib.urlencode(params))
        return HttpResponseRedirect(next_url)


def remote_verify(request):
    """
    verify the user token that friend server sent.
    """
    import urllib
    import hashlib

    from django.contrib.sessions.models import Session
    from django.contrib.auth.models import User

    hash_ = request.GET.get("hash", None)
    token = request.GET.get("token", None)
    service = request.GET.get("service", None)

    if not hash_ or not token or not service:
        return HttpResponseForbidden()

    service = get_object_or_404(Service, name=service, active=True)

    m = hashlib.sha1()
    m.update(token + service.key)

    if hash_ != m.hexdigest():
        return HttpResponseForbidden()

    session = Session.objects.get(session_key=token)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)

    m = hashlib.sha1()
    if user.is_authenticated():
        # TODO: Add more details in this dict
        a = {"username": user.username,
             "first_name": user.first_name,
             "last_name": user.last_name,
             "email": user.email,
            }
        m.update(user.username + service.key)
    else:
        a = {"username": ""}
        m = None

    # TODO: rethink this terminology
    result = {"data": a}
    if m:
        result.update({"hash": m.hexdigest()})
    else:
        result.update({"hash": ""})

    return HttpResponse(json.dumps(result))
