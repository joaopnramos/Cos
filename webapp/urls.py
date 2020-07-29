from django.urls import path
from webapp import views

app_name = "webapp"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("scientist_register/", views.scietist_register, name="scientist_reg"),
    path("donator_register/", views.donator_register, name="donator_reg"),
    path("login/", views.user_login, name="user_login"),
    path("create/", views.ProjectCreateView, name="project_create"),
    path("list/", views.ProjectListView.as_view(), name="list"),
    path("profile/", views.profileScientist, name='profile'),
    ]
