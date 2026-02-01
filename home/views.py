# Django Built-in Modules
from django.db.models import Prefetch

# Local Apps
from faqs.models import Category, FAQ
from faqs.serializers import CategoryWithFAQSerializer
from contractor.models import Contractor
from contractor.serializers import ContractorListSerializer
from project.models import Project
from project.serializers import ProjectListSerializer
from investments.models import InvestmentSale
from investments.serializers import InvestmentSaleDetailSerializer

# Third Party Packages
from rest_framework import generics





# ---------------------------
# 1. نمایش سوالات
# ---------------------------

class FAQPageAPIView(generics.ListAPIView):
    serializer_class = CategoryWithFAQSerializer
    queryset = Category.objects.all().order_by('name').prefetch_related(
        Prefetch("faqs", queryset= FAQ.objects.filter(is_featured= True).order_by('created'))
    )



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




# ---------------------------
# 4. نمایش بازار
# ---------------------------
class InvestmentSaleListAPIview(generics.ListAPIView):

    queryset = InvestmentSale.objects.all()
    serializer_class = InvestmentSaleDetailSerializer











