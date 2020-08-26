from django import forms
from django.contrib.auth.models import User
from .models import *
# from django.core.validators import MinLengthValidator, MaxValueValidator

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
class ScientistForm(forms.Form):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    work_local = forms.CharField(required=True)
    bi = forms.IntegerField(required=True)
    phone = forms.IntegerField(required=True)

    def clean_phone(self, *args, **kwargs):
        phone = self.cleaned_data.get("phone")
        phones = Scientist.objects.order_by("phone")
        for u in phones:
            if u.phone == phone:
                raise forms.ValidationError("this phone already exists")

            else:
                return phone
   

#Form de criar um donator
class DonatorForm(forms.ModelForm):
    class Meta():
        model = Donator
        fields = ("age",)
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('age') <18:
            raise forms.ValidationError('Sorry, but users with age less than 18 can´t register to our website')
        


#Form de um projeto
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', "sensorsChoice", "periodChoice","spacetimeChoice")
        labels = {
        "sensorsChoice": "Choose The Sensor You Need",
        "periodChoice":"Choose How Many Time The Program Will Run",
        "spacetimeChoice": "Choose The period of time beetween data analysis" }

    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    # name = forms.CharField(max_length=100, required=True)

#Form que serve para dar update ao user!
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# class DataForm(forms.Form):
#     file = forms.FileField()





    
 
