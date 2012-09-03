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

import hmac
import hashlib


class HashSum(object):
    """
    Make a hash from data and a secret key that will represent the data health
    in the remote side.
    """

    def __init__(self, key):
        self.key = key

    def sign(self, data, key=None):
        """
        Sign the data with key, and return the result checksum
        """
        return hmac.new(
            self.key or  key,
            data,
            hashlib.sha1).hexdigest()

    def is_valid(self, data, checksum):
        """
        Check the data and checksum.
        """
        a = hmac.new(self.key,
                     data,
                     hashlib.sha1).hexdigest()
        return a == checksum


DefaultValidation = HashSum
