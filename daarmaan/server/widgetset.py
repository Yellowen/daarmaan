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
from vanda.apps.dashboard.widgets.nav import NavigationMenu
from vanda.apps.dashboard.base import dashboard


class TopMenu (NavigationMenu):
    name = "top_menu"
    title = "Navigation"

    navigation_dict = {_("Edit profile"): "/asdfad/",
                       _("Logout"): "/logout/"}


print ">>>> ", TopMenu().to_json()
dashboard.register(TopMenu())
dashboard.add_widget_to('header', TopMenu())
print  "<<<<<<<<<<<< ", dashboard.save_config()
