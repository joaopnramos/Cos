from django.urls import path
from webapp import views
from django.contrib.auth import views as auth_views

app_name = "webapp"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("scientist_register/", views.scietist_register, name="scientist_reg"),
    path("donator_register/", views.donator_register, name="donator_reg"),
    path("login/", views.user_login, name="user_login"),
    path("create/", views.ProjectCreateView, name="project_create"),
    path("list/<int:pk>", views.ProjectDetailView.as_view(), name="detail"),
    path("list/", views.ProjectListView.as_view(), name="list"),
    path("update/<int:pk>", views.ProjectUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.ProjectDeleteView.as_view(), name="delete"),
    path("donator/list_all", views.DonatorList, name="donator_list"),
    path("donator/<int:pk>", views.DataGiveView, name="register_don_project"),
    path("profile/", views.profileScientist, name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='webapp/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='webapp/password_reset_done.html'), name='password_reset_done'),    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='webapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='webapp/password_reset_complete.html'), name='password_reset_complete'),

]
