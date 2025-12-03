from rest_framework import serializers
from .models import Project, ProjectStatus, ProjectDocuments, ProjectProgressReport, Gallery




class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ('id', 'name')

class GallerySerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ReadOnlyField()

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'image_thumbnail', 'alt')

class ProjectProgressReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProgressReport
        fields = ('id', 'pdf', 'project')

class ProjectDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocuments
        fields = ('id', 'pdf', 'project')



class ProjectListSerializer(serializers.ModelSerializer):
    status = ProjectStatusSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'province', 'city', 'profit_to_date', 'invest_start_from', 'estimated_completion_date',
                  'status', 'start_date', )


class ProjectSerializer(serializers.ModelSerializer):
    status = ProjectStatusSerializer(read_only=True)
    gallery = GallerySerializer(many=True, read_only=True)
    progress_reports = ProjectProgressReportSerializer(many=True, read_only=True)
    documents = ProjectDocumentsSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'province', 'city', 'usage_type', 'profit_to_date', 'invest_start_from', 'contractor',
                  'floor_count', 'unit_count', 'usable_area', 'status', 'estimated_completion_date', 'start_date',
                  'project_details', 'address', 'map', 'price_per_metr', 'total_area', 'complete_area', 'bedroom_count',
                  'parking_count', 'warehouse_count', 'gallery', 'progress_reports', 'documents')
        read_only_fields = ('id', 'created')