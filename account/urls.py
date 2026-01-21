# account/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'account'
router = DefaultRouter()

urlpatterns = [
    # مسیرهای APIViews با as_view()
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('send-otp/', views.SendOTPAPIView.as_view(), name= 'send-otp'),
    path('verify-otp/', views.VerifyOTPAPIView.as_view(), name= 'verify-otp'),
    path('verify-national-code/', views.VerifyNationalCodeAPIView.as_view(), name= 'verify-national-code'),
    path('reset-password/set/', views.PasswordResetAPIView.as_view(), name='password_reset_set'),
    path('user/profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name= 'change-password'),
    path('authentication/', views.AuthenticationVerifyAPIView.as_view(), name= 'verify-authenticate'),



    # مسیرهای ViewSet ها از طریق router
    path('', include(router.urls)),
]
