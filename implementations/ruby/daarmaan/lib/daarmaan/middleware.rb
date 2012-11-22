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

require 'uri'

require 'daarmaan/validators'

module Daarmaan

  DefaultValidation = HmacValidation

  # Rack middleware for daarmaan base authentication
  class AuthMiddleware
    
    def initialize app
      @app = app

      # Read the authentication configuration
      daarmaan_setup
      @validator = DefaultValidation.new @daarmaan.key
    end 
    
    def call env

      # Setup session object using already setuped middlewares
      session = env["rack.session"]

      if !session.has_key? :daarmaan
        # Setup the daarmaan object inside session object
        session[:daarmaan] = @daarmaan

      end

      # Create a Rack Request
      request = Rack::Request.new(env)
      params = request.params
      uri = URI(request.url)


      if request.get?
        # In the case of GET request

        # Get the possible ticket, ack and hash parameter
        ticket = params["ticket"]
        ack = params["ack"]
        hash = params["hash"]

        if ack
          # User not authenticated
          params.delete("ack")
          uri.query = URI.encode_www_form(params)
          session["answered"] = true
        end

        if ticket
          # user is authenticated in Daarmaan
          params.delete("ticket")
          params.delete("hash")
          uri.query = URI.encode_www_form(params)
          if hash and @validator.is_valid? ticket, hash
            session[:session_id] = ticket
            user_data = validate(ticket)
            
            first_name = user_data["first_name"]
            if first_name.empty?
              first_name = "unknown"
            end

            last_name = user_data["last_name"]
            if last_name.empty?
              last_name = "unknown"
            end

            email = user_data["email"]
            user = User.where(:login => user_data["username"]).first_or_create!(firstname: first_name,
                                                                                lastname: last_name,
                                                                                mail: user_data["email"])

            session["answered"] = true
            session[:user_id] = user.id
            session[:user] = user
          end

        end

      else
        # Post request should be checked after logging user in or with
        # ticket and ack
      end

      status, headers, body = @app.call(env)
      
      response = Rack::Response.new(body, status,
                                    headers)
      
      if !session.has_key? "redirected"
        if session.has_key? "answered"
          url = uri.to_s
          if params.empty?
            url = url[0..-2]
          end
          response.redirect(url, 301)
          session["redirected"] = true
          session.delete("answered")
        else
          response.redirect(@daarmaan.login_url(uri.to_s), 301)
        end

      else
        session.delete("redirected")
      end

      response.finish
      return response.to_a
    end
    
    private

    # Read the authentication configuration    
    def daarmaan_setup
      if Rails.application.config.auth_config["method"] == "daarmaan"
        @daarmaan = Daarmaan::Server.new Rails.application.config.auth_config
      else
        @daarmaan = Daarmaan::Server.new 
      end
    end
    
    def validate ticket
      url = URI("#{@daarmaan.host}/verification/")
      hash = @validator.sign(ticket)

      params = {
        token: ticket,
        hash: hash,
        service: @daarmaan.service
      }

      url.query = URI.encode_www_form(params)
      begin
        res = Net::HTTP.get_response(url)
      rescue Errno::ECONNRESET
        # TODO: handle this situation
      end

      if res.code == "200"
        json_data = JSON::load res.body
        if json_data.has_key? "hash"
          hash = json_data["hash"]
          data = json_data["data"]
          
          if @validator.is_valid? data["username"], hash
            return data
          else
            return nil
          end
        end
      else
        # TODO: Find the best way to deal with unreachablity
        # of Daarmaan
        # TODO: Add log here
      end

    end
  end

end
