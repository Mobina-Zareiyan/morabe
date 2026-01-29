# Django Built-in Modules
from django.urls import path, include

# Local Apps
from .views import FAQViewSet

# Third Party Packages
from rest_framework.routers import DefaultRouter


app_name = 'faqs'
router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faqs')

urlpatterns = [
    path('', include(router.urls)),
]
