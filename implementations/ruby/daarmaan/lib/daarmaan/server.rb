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

require 'cgi'


module Daarmaan
  # This class represent the Daarmaan authentication server
  class Server

    attr_reader :key, :host, :service

    def initialize kwargs={}
      if !kwargs.empty?
        @host = kwargs["host"] or raise ArgumentError, "specify `host`"
        @host.chomp!("/")

        @service = kwargs["service_name"] or raise ArgumentError, "specify `service_name`"
        @key = kwargs["service_key"] or raise ArgumentError, "specify `service_key`"

        @login_url = kwargs.has_key?("login_url") ? kwargs["login_url"] : "/"
        @login_page = kwargs.has_key?("login_page") ? kwargs["login_page"] : "/"

        @initialized = true
      else
        @initialized = false
      end
    end


    def login_page next_url=nil
      params = "/?service=#{@service}"
      if next_url
        params = "#{params}&next=" + CGI.escape(next_url)
      end
      login_url = @login_page.chomp("/")
      "#{@host}#{login_url}#{params}"
    end

    def login_url next_url=nil
      params = "/?service=#{@service}"
      if next_url
        params = "#{params}&next=" + CGI.escape(next_url)
      end
      login_url = @login_url.chomp("/")
      "#{@host}#{login_url}#{params}"
    end

    def is_used?
      @initialized
    end

  end
end
