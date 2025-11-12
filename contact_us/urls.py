from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactUsViewSet

router = DefaultRouter()
router.register(r'contact_us', ContactUsViewSet, basename='contact_us')

urlpatterns = [
    path('', include(router.urls)),
]
