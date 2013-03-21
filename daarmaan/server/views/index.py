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

from django.shortcuts import render_to_response as rr
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.conf.urls import patterns, url
from django.conf import settings

from daarmaan.server.forms import PreRegistrationForm, NewUserForm, LoginForm
from daarmaan.server.models import VerificationCode


class IndexPage(object):
    """
    Daarmaan index page class.
    """
    template = "index.html"
    register_template = "register.html"
    new_user_form_template = "new_user_form.html"

    @property
    def urls(self):
        """
        First Page url patterns.
        """
        urlpatterns = patterns(
            '',
            url(r"^$", self.index,
                name="home"),
            url(r"^register/$", self.pre_register,
                name="home"),

            url(r"^verificate/([A-Fa-f0-9]{40})/$", self.verificate,
                name="verificate"),
            url(r"^registration/done/$", self.registration_done,
                name="registration-done"),

            )
        return urlpatterns

    def index(self, request):
        """
        Index view.
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard-index'))

        if request.method == "POST":
            return self.login(request)

        else:
            form = LoginForm()
            next_url = request.GET.get("next", "")
            return rr(self.template,
                      {"form": form,
                       "next": next_url},
                      context_instance=RequestContext(request))


    def login(self, request):
        """
        Login view that only accept a POST request.
        """
        next_url = request.POST.get("next", None)

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get("remember_me", False)
            next_url = form.cleaned_data.get("next", None)

            # Authenticate the user
            user = authenticate(username=username,
                               password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    self._setup_session(request)

                    if next_url:
                        return HttpResponseRedirect(next_url)

                    return redirect(reverse(
                        "dashboard-index",
                        args=[]))
                else:
                    return rr(self.template,
                              {"form": form,
                               "msgclass": "text-error",
                               "next": next_url,
                               "msg": _("Your account is disabled.")},
                              context_instance=RequestContext(request))
            else:
                return rr(self.template,
                          {"form": form,
                           "msgclass": "text-error",
                           "next": next_url,
                           "msg": _("Username or Password is invalid.")},
                          context_instance=RequestContext(request))

        else:
            return rr(self.template,
                      {"form": form,
                       "next": next_url},
                       context_instance=RequestContext(request))

    def pre_register(self, request):
        """
        Handle the registeration request.
        """
        from django.contrib.auth.models import User
        from django.db import IntegrityError

        if request.method == "POST":
            form = PreRegistrationForm(request.POST)
            msg = None
            klass = ""
            if form.is_valid():
                # In case of valid information from user.
                email = form.cleaned_data["email"]
                username = form.cleaned_data["username"]

                # Check for email exists
                emails_count = User.objects.filter(email=email).count()
                if emails_count:
                    failed = True
                    msg = _("This email has been registered before.")
                    klass = "text-error"

                else:
                    try:
                        # Create and save an inactive user
                        user = User(username=username,
                                email=email)
                        user.active = False
                        user.save()

                        if settings.EMAIL_VERIFICATION:
                            # Generate and send a verification code to user
                            # only if EMAIL_VERIFICATION was set
                            verif_code = VerificationCode.generate(user)

                            verification_link = reverse("verificate",
                                                        args=[verif_code])

                            print ">>> ", verification_link
                            self.send_verification_mail(user,
                                                        verification_link)

                            msg = _("A verfication mail has been sent to your e-mail address.")
                        else:
                            msg = _("You're request submited, thanks for your interest.")

                        klass = "text-success"
                        form = PreRegistrationForm()
                    except IntegrityError:
                        # In case of exists username
                        msg = _("User already exists.")
                        klass = "text-error"

            return rr(self.register_template,
                  {"form": form,
                   "msg": msg,
                   "msgclass": klass},
                  context_instance=RequestContext(request))
        else:
            form = PreRegistrationForm()
            return rr(self.register_template,
                  {"form": form},
                  context_instance=RequestContext(request))

    def _setup_session(self, request):
        """
        Insert all needed values into user session.
        """
        # TODO: Do we need to set the user services to his session.
        return
        services = request.user.get_profile().services.all()
        services_id = [i.id for i in services]
        request.session["services"] = services_id

    def verificate(self, request, verification_code):
        """
        This view is responsible for verify the user mail address
        from the given verification code and redirect to the basic
        information form view.
        """

        # Look up for given verification code in the VerificationCode
        # model. And check for the validation of an any possible exists
        # code
        try:
            verified_code = VerificationCode.objects.get(
                code=verification_code)
        except VerificationCode.DoesNotExist:
            raise Http404()

        # If the verified_code was valid (belongs to past 48 hours for
        # example) the new user form will allow user to finalize his/her
        # registeration process.
        if verified_code.is_valid():
            form = NewUserForm(initial={
                "verification_code": verified_code.code})

            form.action = reverse("registration-done", args=[])
            return rr(self.new_user_form_template,
                      {"form": form,
                       "user": verified_code.user},
                      context_instance=RequestContext(request))
        else:
            raise Http404()

    def send_verification_mail(self, user, verification_link):
        """
        Send the verification link to the user.
        """
        from django.core.mail import send_mail

        msg = verification_link
        send_mail('[Yellowen] Verification', msg, settings.EMAIL,
                  [user.email], fail_silently=False)

    def registration_done(self, request):
        if request.method == "POST":
            form = NewUserForm(request.POST)
            try:
                verified_code = VerificationCode.objects.get(
                    code = request.POST.get("verification_code", ""))

            except VerificationCode.DoesNotExist:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden()

            if form.is_valid():
                pass1 = form.cleaned_data["password1"]
                pass2 = form.cleaned_data["password2"]
                fname = form.cleaned_data["first_name"]
                lname = form.cleaned_data["last_name"]

                if pass1 != pass2:
                    form._errors = {
                        "password1": _("Two password fields did not match."),
                        "password2": _("Two password fields did not match.")}
                    msg = _("Two password fields did not match.")
                    klass = "text-error"
                elif len(pass1) < 6:
                    form._errors = {
                        "password1": _("Password should be more than 6 character long.")}
                    msg = _("Password should be more than 6 character long.")
                    klass = "text-error"
                elif len(pass1) > 40:
                    form._errors = {
                        "password1": _("Password should be less than 40 character long.")}
                    msg = _("Password should be less than 40 character long.")
                    klass = "text-error"
                else:
                    user = verified_code.user
                    user.set_password(pass1)
                    user.first_name = fname
                    user.last_name = lname
                    user.active = True
                    user.save()

                    # Clean up all the expired codes and currently used one
                    verified_code.delete()
                    VerificationCode.cleanup()

                    # Login the user
                    user = authenticate(username=user.username,
                                        password=pass1)

                    login(request, user)

                    return redirect(reverse(
                        "dashboard-index",
                        args=[]))

            print ">>> ", msg
            return rr(self.new_user_form_template,
                      {"form": form,
                       "user": verified_code.user,
                       "msg": msg,
                       "msgclass": klass},
                      context_instance=RequestContext(request))
        else:
            raise Http404()


index_page = IndexPage()
