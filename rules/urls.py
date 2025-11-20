# rules/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RulesViewSet
app_name = 'rules'
router = DefaultRouter()
router.register(r'rules', RulesViewSet, basename='rules')

urlpatterns = [
    path('', include(router.urls)),
]
