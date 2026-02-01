# Django Built-in Modules
from django.urls import path, include

# Local Apps
from . import views



app_name = 'faqs'

urlpatterns = [
#     path('faqs/categories/',views.FAQCategoryListAPIView.as_view(), name= 'categories'),
#     path("faqs/category/<str:slug>/faqs/", views.FAQByCategoryAPIView.as_view(), name= 'faqs'),
    path('faqs/', views.FAQPageAPIView.as_view(), name= "faqs")
]
