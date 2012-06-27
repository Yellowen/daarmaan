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

from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^authenticate/$', "gauth.views.general.remote_auth",
        name="remote-auth"),
    url(r'^verification/$', "gauth.views.general.remote_verify",
        name="remote-auth"),

    url(r"^login/$", "gauth.views.general.login_view", name="login"),
    url(r'^my/$', "gauth.views.general.dashboard", name="dashboard"),

    url(r"^gstatics/$", "gauth.views.statics.serv_statics",
        name="statics-serv"),
    url(r"^jsonp/validate/$", "gauth.views.statics.ajax_widget_jsonp",
        name="ajax-widget-jsonp"),
    url(r"^$", "gauth.views.general.index", name="home"),

)
