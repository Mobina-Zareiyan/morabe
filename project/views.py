from rest_framework import generics
from .models import Project
from .serializers import ProjectListSerializer, ProjectSerializer



class ProjectListAPIView(generics.ListAPIView):
    queryset = (Project.objects.select_related('status')
                .only(
                    'id', 'title', 'province', 'city', 'profit_to_date', 'invest_start_from', 'estimated_completion_date',
                    'start_date', 'status_id', 'status__id', 'status__name', )
                )

    serializer_class = ProjectListSerializer


class ProjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.prefetch_related('status', 'gallery', 'progress_reports', 'documents')
    serializer_class = ProjectSerializer
    lookup_field = 'slug'


