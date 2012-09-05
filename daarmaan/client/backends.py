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
import urllib2
from urllib import urlencode

from django.conf import settings
from django.contrib.auth.models import User, check_password

from daarmaan.utils import DefaultValidation


class DaarmaanBackend(object):
    """
    Authenticate against the Daarmaan SSO. This class is Django
    authentication backend.
    """

    #: Current client service name
    service = settings.SERVICE_NAME

    #: Client service key
    key = settings.SERVICE_KEY

    #: Daarmaan server url
    daarmaan = settings.DAARMAAN_SERVER

    #: Default validator instance that is responsible for signing and
    #: validating data
    validator = DefaultValidation(key)

    def authenticate(self, **kwargs):
        """
        Try to authenticate to daarmaan SSO using provided informations.
        kwargs dictionary should contains below keys:

        .. option:: token: Actual ticket from daarmaan
        .. option:: request: current request object
        .. option:: hash_: the SHA1 checksum provided by daarmaan.
        """

        token = kwargs.get("token", None)
        request = kwargs.get("request", None)
        hash_ = kwargs.get("hash_", None)

        if not token or not hash_ or not request:
            raise ValueError(
                "You should provide 'request', 'token' and 'hash_' parameters"
                )

        if self.validator.is_valid(token, hash_):
            # If token is signed with hash_
            data = self.validate(token)

            if not data:
                return None
            # Create a user or get the exists one
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
            # If token is not valid
            return None

    def get_user(self, user_id):
        """
        Retreive and return the user object
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def validate(self, token):
        """
        Try to validate the given token for a valid user.
        """
        url = "%s/verification/" % self.daarmaan.lstrip("/")

        hash_ = self.validator.sign(token)

        # Create the request parameters
        params = {"token": token,
                  "hash": hash_,
                  "service": self.service}

        url = "%s?%s" % (url, urlencode(params))

        # Send the request
        try:
            response = urllib2.urlopen(url)
        except urllib2.URLError, e:
            # TODO: Handle the situation on urlerror
            print ">>>> ", e
            response = None

        if response:
            if response.code == 200:
                # If response returned
                json_data = json.loads(response.read())

                if json_data["hash"]:

                    hash_ = json_data["hash"]
                    data = json_data["data"]

                    if self.validator.is_valid(data["username"], hash_):
                        return data
                    else:
                        # TODO: Put some logs here
                        return False

                else:
                    return False
            else:
                # TODO: Find the best way to deal with unreachablity
                # of Daarmaan
                # TODO: Add log here
                return False
        else:
            return False
