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

from daarmaan.server.views.sso import daarmaan_service
from daarmaan.server.views.index import index_page
from daarmaan.server.views.profile import profile

urlpatterns = patterns('',

    #url(r"^login/$", "daarmaan.server.views.general.login_view", name="login"),

    #url(r"^gstatics/$", "daarmaan.server.views.statics.serv_statics",
    #    name="statics-serv"),
    #url(r"^jsonp/validate/$",
    #    "daarmaan.server.views.statics.ajax_widget_jsonp",
    #    name="ajax-widget-jsonp"),

    # Password reset -------------------------
    url(r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset'),

    url(r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),

    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),
    # ----------------------------------------

    url(r"^me/", include(profile.urls)),
    url(r"^\~([A-Za-z][^/]+)/$", profile.view_profile,
        name="view_user_profile"),
    url(r"^", include(index_page.urls)),

    url(r'^', include(daarmaan_service.urls)),
)
