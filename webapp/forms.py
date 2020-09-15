from django import forms
from django.contrib.auth.models import User
from .models import *
from webapp.choices import SENSORS_CHOICES
# from django.core.validators import MinLengthValidator, MaxValueValidator

# Form de criar user em geral!


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ("username", "email", "password")

    def clean(self):
        MIN_LENGTH = 8
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        email = cleaned_data.get("email")
        confirm_password = cleaned_data.get("confirm_password")

        """Serve para verificar se as passwords inseridas são iguais """
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and confirm_password does not match."
            )
        """Serve para verificar se o comprimento da password é o indicado """
        if len(password) < MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % MIN_LENGTH)

        """Serve para verificar se existe pelo menos uma letra e caracter não letra """
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("The new password must contain at least one letter and at least one digit or punctuation character.")


    def clean_email(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError("This email is already in use! Try another email.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if username and User.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError("This username has already been taken!")
        return username



# Form de criar um cientista
class ScientistForm(forms.Form):

    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    address = forms.CharField(required=True, max_length=100)
    work_local = forms.CharField(required=True, max_length=100)
    bi = forms.IntegerField(required=True)
    profile_pic = forms.ImageField(required=False)


# Form de criar um donator
class DonatorForm(forms.ModelForm):
    class Meta():
        model = Donator
        fields = ("age",)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('age') <18:
            raise forms.ValidationError('Sorry, but users with age less than 18 can´t register to our website')



# Form de um projeto
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', "sensorsChoice", "periodChoice","spacetimeChoice")
        labels = {
        "sensorsChoice": "Choose The Sensor You Need",
        "periodChoice":"Choose How Many Time The Program Will Run",
        "spacetimeChoice": "Choose The period of time beetween data analysis" }
    
    name = forms.CharField(required=True, max_length=50)
    sensorsChoice = forms.MultipleChoiceField(choices=SENSORS_CHOICES)

    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":2, "cols":50, 'maxlength': 500}))

# Form que serve para dar update ao user!
class UserUpdateForm(forms.Form):

    email = forms.EmailField(required=False)
    password = forms.CharField( max_length=250, required=False, widget=forms.PasswordInput)

class ScientistUpdate(forms.Form):

    first_name = forms.CharField(required=False, max_length=100)
    last_name = forms.CharField(required=False, max_length=100)
    address = forms.CharField(required=False, max_length=100)
    work_local = forms.CharField(required=False, max_length=100)
    bi = forms.IntegerField(required=False)
    profile_pic = forms.ImageField(required=False)


class SendUsEmail(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":2, "cols":50}))

class SendEmailForm(forms.Form):
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":10, "cols":25}))



