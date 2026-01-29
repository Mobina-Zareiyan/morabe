# Django Built-in Modules
from django.shortcuts import get_object_or_404

# Local Apps
from .models import Category, FAQ
from .serializers import CategorySerializer, FAQSerializer

# third Party Packages
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class FAQViewSet(viewsets.ViewSet):
    """
    ViewSet برای API سوالات متداول:
    - GET /api/faqs/           => دسته‌بندی‌ها و (اختیاری همه FAQ ها)
    - GET /api/faqs/<slug>/    => FAQ های دسته مشخص
    """

    def list(self, request):
        """لیست همه دسته‌ها و اختیاری همه FAQ ها"""
        categories = Category.objects.all().order_by('name')
        category_serializer = CategorySerializer(categories, many=True)

        faqs = FAQ.objects.all().order_by('-created')
        faq_serializer = FAQSerializer(faqs, many=True)

        return Response({
            "categories": category_serializer.data,
            "faqs": faq_serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """نمایش FAQ های یک دسته بر اساس slug"""
        category = get_object_or_404(Category, slug=pk)
        faqs = FAQ.objects.filter(category=category).order_by('-created')
        faq_serializer = FAQSerializer(faqs, many=True)
        return Response({
            "category": CategorySerializer(category).data,
            "faqs": faq_serializer.data
        }, status=status.HTTP_200_OK)
