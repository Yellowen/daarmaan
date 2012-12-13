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

from django.utils.translation import ugettext as _
from vanda.apps.dashboard.widgets.button import Button
from vanda.apps.dashboard.base import dashboard


class UserButton (Button):
    title = _("User Menu")
    name = "user_button"
    image = True
    gravatar = True
    weight = 1000

    css = "/statics/css/bar_button.css"
    js = ["/statics/js/jquery.min.js",
          "/statics/js/bar_button.js"]

    css_class = "bar_button user_button"
    template = "dashboard/widgets/user_button.html"

    def text(self):
        return self.dashboard.request.user.username

    def image_src(self):
        return self.dashboard.request.user.email

    def host(self):
        return self.dashboard.request.META["HTTP_HOST"]


class SettingButton (UserButton):
    title = _("Setting Menu")
    name = "setting_button"
    image = True
    gravatar = False
    weight = 900
    template = "dashboard/widgets/settings_button.html"
    def text(self):
        return False

    def image_src(self):
        return "/statics/image/settings.png"


dashboard.register(UserButton())
dashboard.add_widget_to('header', UserButton())
dashboard.register(SettingButton())
dashboard.add_widget_to('header', SettingButton())

print  "<<<<<<<<<<<< ", dashboard.save_config()
