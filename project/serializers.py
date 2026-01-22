from rest_framework import serializers
from .models import Project, ProjectStatus, ProjectDocuments, ProjectProgressReport, Gallery




class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ('id', 'name')

class GallerySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url= True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'thumbnail_url', 'alt')

    def get_thumbnail_url(self, obj):
        if not getattr(obj, 'image_thumbnail', None):
            return None
        try:
            return obj.image_thumbnail.url
        except (ValueError, FileNotFoundError):
            return None


class ProjectProgressReportSerializer(serializers.ModelSerializer):
    pdf = serializers.FileField(use_url= True)

    class Meta:
        model = ProjectProgressReport
        fields = ('id', 'pdf')

class ProjectDocumentsSerializer(serializers.ModelSerializer):
    pdf = serializers.FileField(use_url= True)

    class Meta:
        model = ProjectDocuments
        fields = ('id', 'pdf')



class ProjectListSerializer(serializers.ModelSerializer):
    status = ProjectStatusSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'province', 'city', 'profit_to_date', 'invest_start_from', 'estimated_completion_date',
                  'status', 'start_date', 'is_featured', 'slug' )



class ContractProjectListSerializer(serializers.ModelSerializer):
    status = ProjectStatusSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'province', 'city', 'profit_to_date', 'invest_start_from', 'estimated_completion_date',
                  'status', 'start_date', 'is_featured', 'contractors')




class ProjectSerializer(serializers.ModelSerializer):
    status = ProjectStatusSerializer(read_only=True)
    gallery = GallerySerializer(many=True, read_only=True)
    progress_reports = ProjectProgressReportSerializer(many=True, read_only=True)
    documents = ProjectDocumentsSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'province', 'city', 'usage_type', 'profit_to_date', 'invest_start_from', 'contractors',
                  'floor_count', 'unit_count', 'usable_area', 'status', 'estimated_completion_date', 'start_date',
                  'project_details', 'address', 'map', 'price_per_meter', 'total_area', 'complete_area', 'bedroom_count',
                  'parking_count', 'warehouse_count', 'gallery', 'progress_reports', 'documents')
        read_only_fields = ('id', 'created')