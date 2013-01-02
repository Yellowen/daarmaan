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
from django.template import RequestContext, Context
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.conf.urls import patterns, url
from vanda.apps.dashboard.widgets.base import Widget
from vanda.apps.dashboard.base import dashboard

from daarmaan.server.models import UserServices, Service
from local_widgets.forms.ublog import SettingsForm


class UltraBlog(Widget):
    title = _("Ultra Blog")
    name = "ultra_blog_widget"
    template = "dashboard/widgets/ultra_blog.html"

    service_name = "ultrablog.com"

    pre_js = ["/statics/js/jquery.hashchange.min.js",
          "/statics/js/jquery.easytabs.min.js"]

    settings_form = SettingsForm()

    @property
    def url_patterns(self):
        return [
            url("^settings/$", self.settings_view,
                name="ublog-settings-view"),
            ]

    def settings_view(self, request):
        return HttpResponse()

    def class_name(self):
        return self.__class__.__name__.lower()

    def widget_html(self, request):
        self._request = request
        html = self.get_html()

        self.problem = False

        try:
            blog_service = Service.objects.get(name=self.service_name)
        except Service.DoesNotExist:
            self.msg = _("Bad Blog Parameters.")
            self.problem = True
            return HttpResponse(html.render(Context({"self": self})))

        try:

            services = UserServices.objects.get(
                user=request.user).services.all()

            if not blog_service in services:
                self.problem = True
                self.msg = _("You don't have access to blog service.")
        except UserServices.DoesNotExist:
            self.problem = True
            self.msg = _("You don't have access to blog service.")
            
        return HttpResponse(html.render(Context({"self": self})))


dashboard.register(UltraBlog())
