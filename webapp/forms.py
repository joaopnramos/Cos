from django import forms
from django.contrib.auth.models import User
from .models import *


# from django.core.validators import MinLengthValidator, MaxValueValidator

# Form de criar user em geral!
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ("username", "email", "password")

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


# Form de criar um cientista
class ScientistForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    work_local = forms.CharField(required=True)
    bi = forms.IntegerField(required=True)
    phone = forms.IntegerField(required=True)


# Form de criar um donator
class DonatorForm(forms.ModelForm):
    class Meta:
        model = Donator
        fields = ("age",)

    def clean(self):
        if int(self.cleaned_data['age']) < 18:
            raise forms.ValidationError('underage!')
        return self.cleaned_data


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')
    # description = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    # name = forms.CharField(max_length=100, required=True)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

