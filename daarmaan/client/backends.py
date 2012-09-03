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

# This file is a part of Daarmaan Global authentication service.
import pickle
import json
import hashlib
from urllib import urlencode
import urllib2

from django.conf import settings
from django.contrib.auth.models import User, check_password


class DaarmaanBackend(object):
    """
    Authenticate against the Daarmaan gauth.
    """
    service = settings.SERVICE_NAME
    key = settings.SERVICE_KEY
    daarmaan = settings.DAARMAAN_SERVER

    def authenticate(self, **kwargs):
        """
        Try to authenticate to daarmaan SSO using provided informations.
        kwargs dictionary should contains below keys:

        token: Actual ticket from daarmaan
        request: current request object
        hash_: the SHA1 checksum provided by daarmaan.
        """
        token = kwargs.get("token", None)
        request = kwargs.get("request", None)
        hash_ = kwargs.get("hash_", None)

        if not token or not hash_ or not request:
            raise ValueError("You should provide 'request', 'token' and 'hash_' parameters")

        if self.is_valid(token, hash_):
            data = self.validate(token)
            user, created = User.objects.get_or_create(
                username=data["username"]
                )
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]

            if created:
                user.pk = data["id"]
                user.save()
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def is_valid(self, token, hash_):
        """
        Check for token and hash integrity.
        """
        key = settings.SERVICE_KEY
        m = hashlib.sha1()
        m.update(token + key)
        if hash_ == m.hexdigest():
            return True
        return False

    def validate(self, token):
        """
        Try to validate the given token for a valid user.
        """
        url = "%s/verification/" % self.daarmaan.lstrip("/")

        # Create the request parameters
        m = hashlib.sha1()
        m.update(token + self.key)
        hash_ = m.hexdigest()
        params = {"token": token,
                  "hash": hash_,
                  "service": self.service}

        url = "%s?%s" % (url, urlencode(params))

        # Send the request
        response = urllib2.urlopen(url)

        if response.code == 200:
            # If response returned
            json_data = json.loads(response.read())

            if json_data["hash"]:
                hash_ = json_data["hash"]
                data = json_data["data"]
                m = hashlib.sha1()
                m.update(data["username"] + self.key)

                if m.hexdigest() == hash_:
                    return data
                else:
                    # TODO: Put some logs here
                    return False

            else:
                return False
        else:
            # TODO: Find the best way to deal with unreachablity of Daarmaan
            pass
