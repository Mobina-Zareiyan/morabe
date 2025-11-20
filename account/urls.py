# account/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'account'
router = DefaultRouter()

urlpatterns = [
    # مسیرهای APIViews با as_view()
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/reset-password/check/', views.PasswordResetCheckView.as_view(), name='password_reset_check'),
    path('auth/reset-password/set/', views.PasswordResetView.as_view(), name='password_reset_set'),
    path('user/profile/', views.ProfileView.as_view(), name='profile'),

    # مسیرهای ViewSet ها از طریق router
    path('', include(router.urls)),
]
