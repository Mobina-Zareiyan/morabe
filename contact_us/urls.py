# Django Built-in Modules
from django.urls import path, include

# Local Apps
from . import views


app_name = 'contact_us'

urlpatterns = [
    path("contact_us/", views.ContactUsMessageAPIView.as_view(), name= "contact-us"),
    path("contact_us/detail/", views.ContactUsPageDetail.as_view(), name= "page-detail"),
]
