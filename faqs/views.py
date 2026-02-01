# Django Built-in Modules
from django.shortcuts import get_object_or_404

# Local Apps
from .models import Category, FAQ
from .serializers import CategoryWithFAQSerializer


# third Party Packages
from rest_framework import generics



# class FAQCategoryListAPIView(generics.ListAPIView):
#     queryset = Category.objects.all().order_by('name').prefetch_related('faqs')
#     serializer_class = CategorySerializer
#
#
# class FAQByCategoryAPIView(generics.ListAPIView):
#     serializer_class = FAQSerializer
#
#     def get_queryset(self):
#         category = get_object_or_404(Category, slug= self.kwargs['slug'])
#         return FAQ.objects.filter(category= category).order_by('created')
#
#


class FAQPageAPIView(generics.ListAPIView):
    serializer_class = CategoryWithFAQSerializer
    queryset = Category.objects.all().order_by('name').prefetch_related("faqs")



