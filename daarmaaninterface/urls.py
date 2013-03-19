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

import os

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from vanda.apps.dashboard.base import dashboard


admin.autodiscover()
dashboard.auto_discovery()


urlpatterns = patterns('',
                       url(r"^my/", include(dashboard.urls)),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r"^", include("daarmaan.server.urls")),

)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
        (r'^statics/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(os.path.dirname(__file__),\
                                        'statics').replace('\\', '/')}),
)
