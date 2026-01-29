# Django Built-in Modules
from django.urls import path, include

# Local Apps
from . import views

# Third Party Packages
from rest_framework.routers import DefaultRouter

app_name = 'contact_us'
router = DefaultRouter()
router.register(r'contact-us', views.ContactUsViewSet, basename='contact-us')

urlpatterns = [
    path('', include(router.urls)),
]
