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

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings


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
    User profile model related to each service.
    """

    user = models.ForeignKey("auth.User",
                             verbose_name=_("permissions"))

    service = models.ForeignKey(Service,
                                verbose_name=_("service"))

    _profile_data = models.TextField(_("service profile"))

    @property
    def data(self):
        return json.loads(self._profile_data)

    @data.setter
    def data(self, value):
        self._profile_data = json.dumps(value)
        return json.dumps(value)

    def __unicode__(self):
        return self.user.username

    class Meta:
        unique_together = ["user", "service"]
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")


class UserServices(models.Model):
    """
    Services that user have access to.
    """
    user = models.ForeignKey("auth.User",
                             verbose_name=_("permissions"))

    services = models.ManyToManyField(Service,
                                      verbose_name=_("service"))

    def __unicode__(self):
        return "%s services" % self.user

    class Meta:
        verbose_name = _("user services")
        verbose_name_plural = _("user services")


class VerificationCode (models.Model):
    """
    Verification code model. This model will contain all the
    verification codes that will sent to users.
    """
    user = models.ForeignKey("auth.User",
                             verbose_name=_("permissions"),
                             unique=True)

    code = models.CharField(_("code"), max_length=40)

    timestamp = models.DateTimeField(auto_now_add=True)

    # 48 houres
    DEFAULT_VALID_TIME = 48

    @classmethod
    def cleanup(cls):
        from datetime import timedelta, datetime

        valid_time = getattr(settings, 'VALIDATION_TIME',
                             cls.DEFAULT_VALID_TIME)

        pasted_48 = datetime.now() - timedelta(hours=valid_time)

        cls.objects.filter(timestamp__lt=pasted_48).delete()

    @classmethod
    def generate(cls, user):
        """
        Generate a verification code. At first look for exists
        valid code.
        """
        try:
            # Is there any exists verification code for given user?
            code = cls.objects.get(user=user)

            if code.is_valid():
                # If code was valid
                return code.code
            else:
                # If code is not valid we need to generate a new one
                # so cleanup all the expired codes
                cls.cleanup()

        except cls.DoesNotExist:
            pass

        # We have to create a new verification code
        import hashlib
        from datetime import datetime

        m = hashlib.sha1()
        m.update("%s%s" % (user.username,
                           datetime.now()))
        code = cls(user=user, code=m.hexdigest())
        code.save()
        return code.code

    def _valid_range(self):
        """
        Returns a valid range of time.
        """
        from datetime import timedelta, datetime

        valid_time = getattr(settings, 'VALIDATION_TIME',
                             self.DEFAULT_VALID_TIME)

        return datetime.now() - timedelta(hours=valid_time)

    def is_valid(self):
        """
        Does verification code belongs to a valid time range.
        """
        pasted_48 = self._valid_range()

        pasted_48.tzinfo = self.timestamp.tzinfo
        print "<<<<< ", self.timestamp, pasted_48
        if self.timestamp < pasted_48:
            return False

        return True
