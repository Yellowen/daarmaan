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
from vanda.apps.dashboard.widgets.button import Button
from vanda.apps.dashboard.base import dashboard

from forms.config import ConfigForm


class UserButton (Button):
    title = _("User Menu")
    name = "user_button"
    image = True
    gravatar = True
    weight = 1000

    css = "/statics/css/bar_button.css"
    #js = "/statics/js/bar_button.js"

    css_class = "bar_button user_button"
    template = "dashboard/widgets/user_button.html"

    def text(self):
        return self.request.user.username

    def image_src(self):
        return self.request.user.email

    def host(self):
        return self.request.META["HTTP_HOST"]


class SettingButton (UserButton):
    title = _("Setting Menu")
    name = "setting_button"
    image = True
    gravatar = False
    weight = 900
    template = "dashboard/widgets/settings_button.html"
    form = ConfigForm

    @property
    def url_patterns(self):
        from django.conf.urls import url
        return [
            url('^config/form/$', self.config_form),
            ]

    def text(self):
        return False

    def image_src(self):
        return "/statics/image/settings.png"

    # Views -------------------------------
    def config_form(self, request):
        if request.method == "POST":
            pass
        else:
            form = self.form()
            return rr(form.template,
                    {"form": form,
                     "self": self},
                    context_instance=RequestContext(request))


class AddWidgetButton (UserButton):
    title = _("Widget Menu")
    name = "add_widget"
    image = True
    gravatar = False
    weight = 800
    template = "dashboard/widgets/settings_button.html"

    @property
    def url_patterns(self):
        from django.conf.urls import url
        return [
            url('^list/$', self.widgets_list),
            ]

    def text(self):
        return False

    def image_src(self):
        return "/statics/image/add.png"

    # Views -------------------------------
    def widgets_list(self, request):
        widgets = list(self.dashboard.widgets)
        #widgets = [i.name for i in widgets]
        return rr("dashboard/widgets/add_widgets.html",
                  {"widgets": widgets,
                   "self": self},
                  context_instance=RequestContext(request))


dashboard.register(UserButton())
dashboard.add_widget_to('header', UserButton())
dashboard.register(AddWidgetButton())
dashboard.add_widget_to('header', AddWidgetButton())
dashboard.register(SettingButton())
dashboard.add_widget_to('header', SettingButton())
