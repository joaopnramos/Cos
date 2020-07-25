from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


#Start View



class RegisterView(TemplateView):
    template_name = "webapp/generic_register.html"


#Registro do Cientista!!
#
#
def scietist_register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        scientist_form = ScientistForm(data=request.POST)
        if user_form.is_valid() and scientist_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            scientist_profile = scientist_form.save(commit=False)
            scientist_profile.user = user
            scientist_profile.save()
            registered = True
        else:
            print(user_form.errors, scientist_form.errors)
            print("deu merda")
    else:
        user_form = UserForm
        scientist_form = ScientistForm

    return render(request, "webapp/registration_scientist.html", 
                                {"user_form":user_form,
                                 "scientist_form":ScientistForm,
                                 "registered": registered})

#Registro do donator!
#
#
def donator_register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        donator_form = DonatorForm(data=request.POST)
        if user_form.is_valid() and donator_form.is_valid():
        
            if int(donator_form["age"].value()) < 18:
                return render(request, "webapp/registration_donator.html",{"underage":True})

          
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            donator_profile = donator_form.save(commit=False)
            donator_profile.user = user
            donator_profile.save()
            registered = True
        else:
            print(user_form.errors, donator_form.errors)
            print("deu merda")
    else:
        user_form = UserForm
        donator_form = DonatorForm

    return render(request, "webapp/registration_donator.html", 
                                {"user_form":user_form,
                                 "donator_form":donator_form,
                                 "registered": registered})


#Login generalista
def user_login(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("someone try to login and fail")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "webapp/login.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

