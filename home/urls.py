from django.urls import path
from . import views

app_name = "home"


urlpatterns = [
    path("home-questions/", views.FAQViewSet.as_view(), name= "h-questions"),
    path("home-Contractor/", views.ContractorListAPIView.as_view(), name= "h-Contractor"),
    path("home-project/", views.ProjectListAPIView.as_view(), name= "h-project"),
]