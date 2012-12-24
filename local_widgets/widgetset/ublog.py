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

from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.http import HttpResponse
from vanda.apps.dashboard.widgets.base import Widget
from vanda.apps.dashboard.base import dashboard


class UltraBlog(Widget):
    title = _("Ultra Blog")
    name = "ultra_blog_widget"
    template = "dashboard/widgets/ultra_blog.html"

    pre_js = ["/statics/js/jquery.hashchange.min.js",
          "/statics/js/jquery.easytabs.min.js"]


dashboard.register(UltraBlog())
