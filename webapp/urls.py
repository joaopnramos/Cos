from django.urls import path, include
from webapp import views
from .views import CustomObtainAuthToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("dataStart", views.DataViewSet, basename="Data-viewset")
router.register("dataGiveStart", views.DataGiveViewSet, basename="DataGive-viewset")
router.register("projectStart", views.ProjectViewSet, basename="Project-viewset")
router.register("DonatorStart", views.DonatorViewSet, basename="Donator-viewset")

app_name = "webapp"



urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path('api-token-auth/', CustomObtainAuthToken.as_view()),
    path("list/<int:pk>", views.ProjectDetailView.as_view(), name="detail"),
    path('apks/', views.download_apk, name='download_apk'),
    path("faq/", views.faq, name="faq"),
    path("datagivedelete/<int:pk>", views.donator_exit_project, name= "datagivedelete"),
   
    path("",include(router.urls)),
    path("scientist_register/", views.scientist_register, name="scientist_reg"),
    path("profile/", views.profileScientist, name='profile'),
    path("myscientistprojects/", views.privateScientistProjectView, name="mySprojects"),
    path("myscientistprojects/<int:pk>", views.ProjectDetailView.as_view(), name="scientist_list_detail"),
    path("create/", views.ProjectCreateView, name="project_create"),
    path("list/", views.ProjectListView.as_view(), name="list"),
    path("update/<int:pk>", views.ProjectUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.ProjectDeleteView.as_view(), name="delete"),
    path("finishingview/finish/<int:pk>", views.finishthedproject, name="finish"),
    path("list/archived", views.MyArchivedProjectsS, name="archived_list"),
    path("list/active", views.MyActiveProjectsS, name="active_list"),
    path("finishingview/<int:pk>", views.FinalizingView, name="finalizing"),
    
    path("donator/list_all", views.DonatorList, name="donator_list"),
    path("donator/list_all/archived", views.MyArchivedProjectsD, name="donator_list_arc"),
    path("donator/list_all/active", views.MyActiveProjectsD, name="donator_list_act"),
    path("donator/<int:pk>", views.DataGiveView, name="register_don_project"),
    path("donator/mydonatorprojects/", views.privateDonatorProjectView, name="myDprojects"),
    path("donator/mydonatorprojects/<int:pk>", views.ProjectDetailView.as_view(), name="donator_list_detail"),
    path("donator_register/", views.donator_register, name="donator_reg"),
    path("export_data/<int:pk>", views.export_data, name="export_data"),
    path("password/", views.PasswordChangedView.as_view(), name= "p_changed"),
    path("sprofile/<int:pk>", views.see_scientist_profile, name="sprofile")

    # path("uploaddonatorfiles/<int:pk>", views.uploadDonatorFilesView, name="uploadFiles"),
]
