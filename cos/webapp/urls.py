from django.urls import path
from webapp import views

app_name = "webapp"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("scientist_register/", views.scietist_register, name="scientist_reg"),
    path("donator_register/", views.donator_register, name="donator_reg"),
]
