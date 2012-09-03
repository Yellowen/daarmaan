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

from django.db import models
from django.utils.translation import ugettext as _


class SSOSession(models.Model):
    session = models.CharField(_("session"),
                               unique=True,
                               max_length=64)
    sso_session = models.CharField(_("SSO Session"),
                                   max_length=64)
    user = models.ForeignKey("auth.User",
                             verbose_name=_("user"))

    def __unicode__(self):
        return "%s = %s" % (self.session,
                            self.sso_session)

    class Meta:
        verbose_name = _("SSO Session")
        verbose_name_plural = _("SSO sessions")
