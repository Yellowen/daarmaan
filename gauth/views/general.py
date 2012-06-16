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

from django.shortcuts import render_to_response as rr
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from gauth.forms import LoginForm


def dashboard(request):
    return HttpResponse()


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    form = LoginForm(request.POST)

    user = authenticate(username=username,
                        password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(reverse("gauth.views.general.dashboard", args=[]))
        else:
            return rr("index.html", {"loginform": form,
                                     "msgclass": "error",
                                     "msg": _("Your account is disabled.")},
                          context_instance=RequestContext(request))

    else:
        return rr("index.html", {"loginform": form,
                                 "msgclass": "error",
                                 "msg": _("Username or Password is invalid.")},
                  context_instance=RequestContext(request))


def pre_register(request):
    return HttpResponse()


def index(request):
    """
    Main page.
    """
    if request.method == "POST":
        if request.POST["submit"] == "login":
            return login_view(request)
        else:
            return pre_register(request)
    else:
        form = LoginForm()
        return rr("index.html", {"loginform": form},
                  context_instance=RequestContext(request))
