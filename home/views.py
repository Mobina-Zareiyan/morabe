# Django Module
from drf_spectacular.helpers import forced_singular_serializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404


# Local Module
from questions.models import Category, FAQ
from questions.serializers import CategorySerializer, FAQSerializer
from contractor.models import Contractor
from contractor.serializers import ContractorListSerializer
from project.models import Project
from project.serializers import ProjectListSerializer




# ---------------------------
# 1. نمایش سوالات
# ---------------------------

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

        faqs = FAQ.objects.filter(is_featured= True).order_by('-created')
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





# ---------------------------
# 2. نمایش سازندگان
# ---------------------------

class ContractorListAPIView(generics.ListAPIView):
    queryset = Contractor.objects.filter(is_featured= True)
    serializer_class = ContractorListSerializer



# ---------------------------
# 3. نمایش پروژه‌ها
# ---------------------------
class ProjectListAPIView(generics.ListAPIView):
    queryset = (Project.objects.filter(is_featured= True).select_related('status')
                .only(
                    'id', 'title', 'profit_to_date', 'invest_start_from', 'estimated_completion_date',
                    'start_date', 'is_featured', 'status_id', 'status__id', 'status__name',
                    'province__id', 'province__name', 'city__id', 'city__name' )
                )

    serializer_class = ProjectListSerializer












