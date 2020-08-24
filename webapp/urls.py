from django.urls import path
from webapp import views
from rest_framework.authtoken.views import obtain_auth_token 

app_name = "webapp"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("list/<int:pk>", views.ProjectDetailView.as_view(), name="detail"),

    
    path("scientist_register/", views.scietist_register, name="scientist_reg"),
    path("profile/", views.profileScientist, name='profile'),
    path("myscientistprojects/", views.privateScientistProjectView, name="mySprojects"),
    path("myscientistprojects/<int:pk>", views.ProjectDetailView.as_view(), name="scientist_list_detail"),
    path("create/", views.ProjectCreateView, name="project_create"),
    path("list/", views.ProjectListView.as_view(), name="list"),
    path("update/<int:pk>", views.ProjectUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.ProjectDeleteView.as_view(), name="delete"),
    path("finish/<int:pk>", views.finishthedproject, name="finish"),
    
    #path("donator/list_all/archived", views.DonatorList, name="donator_list"),
    #path("donator/list_all/active", views.DonatorList, name="donator_list"),
    path("donator/list_all", views.DonatorList, name="donator_list"),
    path("donator/<int:pk>", views.DataGiveView, name="register_don_project"),
    path("donator/mydonatorprojects/", views.privateDonatorProjectView, name="myDprojects"),
    path("donator/mydonatorprojects/<int:pk>", views.ProjectDetailView.as_view(), name="donator_list_detail"),
    path("donator_register/", views.donator_register, name="donator_reg"),
    
    
    
    # path("uploaddonatorfiles/<int:pk>", views.uploadDonatorFilesView, name="uploadFiles"),
]
