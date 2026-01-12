from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet


app_name = "home"
router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faqs')


urlpatterns = [
    # path("questions/", views.FAQViewSet.as_view(), name= "h-questions"),
    path("contractor/", views.ContractorListAPIView.as_view(), name= "h-Contractor"),
    path("project/", views.ProjectListAPIView.as_view(), name= "h-project"),
    path('', include(router.urls)),
]