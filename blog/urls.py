# Django Built-in Modules
from django.urls import path

# Local Apps
from . import views


app_name = 'blog'

urlpatterns = [
    path('blogs/', views.BlogListAPIView.as_view(), name='blog-list'),
    path('blogs/<int:id>/', views.BlogDetailAPIView.as_view(), name='blog-detail'),
    path('blogs/<int:id>/comments/', views.BlogCommentCreateAPIView.as_view(), name='blog-comment-create'),
]
