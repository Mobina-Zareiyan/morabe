# Django Built-in Modules
from django.urls import path, include

# local Apps
from . import views

# Third Party Packages


app_name = "home"


urlpatterns = [
    path("contractor/", views.ContractorListAPIView.as_view(), name= "h-Contractor"),
    path("project/", views.ProjectListAPIView.as_view(), name= "h-project"),
    path('investment/sale/',views.InvestmentSaleListAPIview.as_view(), name= "h-investment"),
    path('faqs/', views.FAQPageAPIView.as_view(), name="faqs")
]