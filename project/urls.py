# Django Built-in Modules
from django.urls import path

# Local Apps
from . import views

app_name = 'project'

urlpatterns = [
    path('projects/', views.ProjectListAPIView.as_view(), name='project-list'),
    path('project/<str:slug>/', views.ProjectDetailAPIView.as_view(), name='project-detail'),
]
