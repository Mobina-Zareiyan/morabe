# Django Built-in Modules
from django.urls import path

# Local Apps
from . import views

app_name = 'contractor'

urlpatterns = [
    path('contractors/', views.ContractorListAPIView.as_view(), name='contractor-list'),
    path('contractor/<str:slug>/', views.ContractorDetailAPIView.as_view(), name='contractor-detail'),
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
]
