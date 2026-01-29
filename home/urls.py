# Django Built-in Modules
from django.urls import path, include

# local Apps
from . import views
from .views import FAQViewSet

# Third Party Packages
from rest_framework.routers import DefaultRouter


app_name = "home"
router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faqs')


urlpatterns = [
    # path("questions/", views.FAQViewSet.as_view(), name= "h-questions"),
    path("contractor/", views.ContractorListAPIView.as_view(), name= "h-Contractor"),
    path("project/", views.ProjectListAPIView.as_view(), name= "h-project"),
    path('investment/sale/',views.InvestmentSaleListAPIview.as_view(), name= "h-investment"),
    path('', include(router.urls)),
]