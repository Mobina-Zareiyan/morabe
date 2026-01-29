# Django Built-in Modules
from django.urls import path, include

# Local Apps
from .views import RulesViewSet

# Third Party Packages
from rest_framework.routers import DefaultRouter


app_name = 'rules'
router = DefaultRouter()
router.register(r'rules', RulesViewSet, basename='rules')

urlpatterns = [
    path('', include(router.urls)),
]
