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
import urllib

from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from captcha.fields import ReCaptchaField

from daarmaan.server.models import BasicProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32,
                               label=_("username"))
    password = forms.CharField(max_length=64,
                               label=_("password"),
                               widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label=_("Remember me"), required=False)
    next_ = forms.CharField(required=False)


class PreRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, label=_("Username"))
    email = forms.EmailField(label=_("Email"))
    captcha = ReCaptchaField(attrs={"theme" : 'custom',
                                    "custom_theme_widget": 'recaptcha_widget'})


class PostRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_("First Name"))
    last_name = forms.CharField(max_length=30, label=_("Last Name"))
    password1 = forms.CharField(max_length=250, label=_("Password"),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=250, label=_("Enter again"),
                                widget=forms.PasswordInput())

    def save(self, user):
        """
        Save the cleaned data to User model.
        """
        if not user:
            raise self.NoUser()

        data = self.cleaned_data
        if not data["password1"] == data["password2"]:
            raise self.PasswordError(_("You entered two different passwords"))

        password = data["password1"]
        if len(password) < 6:
            raise self.PasswordError(
                _("Password length should be more than six charachters"))

        user.set_password(password)
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()

        return True

    class NoUser(Exception):
        pass

    class PasswordError(Exception):
        pass


class NewUserForm (forms.Form):
    """
    This form will collect the basic user information
    after email verification.
    """

    first_name = forms.CharField(label=_("first name"),
                                 max_length=32, required=False)
    last_name = forms.CharField(label=_("last name"),
                                max_length=32, required=False)
    password1 = forms.CharField(label=_("password"),
                                max_length=32,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("repead password"),
                                max_length=32,
                                widget=forms.PasswordInput())
    verification_code = forms.CharField(widget=forms.HiddenInput(),
                                        max_length=40)


class EditBasicProfile(forms.ModelForm):
    """
    Form for editing the basic information of user.
    """
    first_name = forms.CharField(label=_("First name"),
                                 max_length=30,
                                 required=False)
    last_name = forms.CharField(label=_("last name"),
                                max_length=30,
                                required=False)

    def __init__(self, user=None, *args, **kwargs):

        if user:

            # TODO: Add the profile data to initial dict too
            data = {"first_name": user.first_name,
                    "last_name": user.last_name}

            super(EditBasicProfile, self).__init__(initial=data, *args,
                                                   **kwargs)
        else:
            super(EditBasicProfile, self).__init__(*args,
                                                   **kwargs)

    def save(self, *args, **kwargs):
        obj = super(EditBasicProfile, self).save(commit=False)
        obj.user.first_name = self.cleaned_data["first_name"]
        obj.user.last_name = self.cleaned_data["last_name"]
        obj.user.save()
        obj.save()

    class Meta:
        model = BasicProfile
        exclude = ["user", ]
