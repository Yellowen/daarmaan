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
from urllib import urlencode

from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout as django_logout
from django.conf import settings


def logout(request):
    """
    Logout the user and redirect him/her to daarmaan.
    """
    django_logout(request)
    request.session["redirected"] = request.path.split("?")[0]
    host = "http://%s" % request.get_host()
    next_ = request.GET.get("next", host)

    next_url = "&%s" % urlencode({"next": next_})

    url = "%s?service=%s%s&ack=" % (settings.LOGOUT_URL,
                             settings.SERVICE_NAME,
                             next_url)

    return HttpResponsePermanentRedirect(url)
