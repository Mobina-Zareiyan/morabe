from django.urls import path
from . import views

app_name = 'contractor'

urlpatterns = [
    path('contractors/', views.ContractorListAPIView.as_view(), name='contractor-list'),
    path('contractor/<slug:slug>/', views.ContractorDetailAPIView.as_view(), name='contractor-detail'),
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
]
