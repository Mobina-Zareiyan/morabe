from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'contact_us'
router = DefaultRouter()
router.register(r'contact-us', views.ContactUsViewSet, basename='contact-us')

urlpatterns = [
    path('', include(router.urls)),
]
