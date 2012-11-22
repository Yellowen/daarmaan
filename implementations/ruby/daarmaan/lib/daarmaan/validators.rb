# -----------------------------------------------------------------------------
# Daarmaan - Ruby implementation of Daarmaan SSO client
# Copyright (C) 2012  Yellowen Inc
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
# -----------------------------------------------------------------------------


module Daarmaan

  # Default data signing class using hmac algorithm
  class HmacValidation
    
    def initialize key
      @key = key

    end
    
    # Check the validation of given data and hash
    def is_valid? data, hash
      my_hash = OpenSSL::HMAC.hexdigest(OpenSSL::Digest::Digest.new('sha1'),
                                     @key, data)
      hash == my_hash
    end

    # Sign the data with default or given key, and return the hash
    def sign data, key=nil
      k = @key
      if key
        k = key
      end

      OpenSSL::HMAC.hexdigest(OpenSSL::Digest::Digest.new('sha1'),
                                     k, data)
    end
  end
end
