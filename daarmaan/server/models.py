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


class Service(models.Model):
    """
    Service class represent a web application that use Daarmaan as its
    authentication service.
    """
    name = models.CharField(_("service"),
                            max_length=64)
    key = models.CharField(_("key"),
                           max_length=256)

    active = models.BooleanField(_("active"),
                                default=False)

    user = models.ForeignKey('auth.User', verbose_name=_("User"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("Services")


class Profile(models.Model):
    """
    User profile model.
    """

    user = models.ForeignKey("auth.User",
                                    verbose_name=_("permissions"))

    services = models.ManyToManyField(Service,
                                      verbose_name=_("service"))

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
