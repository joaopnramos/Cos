from django import forms
from django.contrib.auth.models import User
from .models import *

#Form de criar user em geral!
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

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

#Form de criar um cientista
class ScientistForm(forms.ModelForm):
    class Meta():
        model = Scientist
        fields = ("phone", "first_name", "last_name", "work_local", "bi", "address")
        

#Form de criar um donator
class DonatorForm(forms.ModelForm):
    class Meta():
        model = Donator
        fields = ("age",)
        