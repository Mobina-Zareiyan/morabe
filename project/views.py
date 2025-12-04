from rest_framework import generics
from .models import Project
from .serializers import ProjectListSerializer, ProjectSerializer



class ProjectListAPIView(generics.ListAPIView):
    queryset = (Project.objects.select_related('status')
                .only(
                    'id', 'title', 'profit_to_date', 'invest_start_from', 'estimated_completion_date',
                    'start_date', 'is_featured', 'status_id', 'status__id', 'status__name',
                    'province__id', 'province__name', 'city__id', 'city__name' )
                )

    serializer_class = ProjectListSerializer


class ProjectDetailAPIView(generics.RetrieveAPIView):
    queryset = (Project.objects.select_related('province', 'city', 'status')
                .prefetch_related('gallery', 'progress_reports', 'documents', 'contractors'))
    serializer_class = ProjectSerializer
    lookup_field = 'slug'


