from rest_framework import serializers
from .models import RegistrationContractor, Gallery, Contractor
from project.serializers import ContractProjectListSerializer


class GallerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ('id', 'image_url', 'thumbnail_url', 'alt', 'title', 'subtitle',)

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_thumbnail_url(self, obj):
        try:
            if obj.image_thumbnail:
                return obj.image_thumbnail.url
        except:
            pass
        return None



class ContractorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'name', 'image', 'successful_project', 'work_experience', 'subtitle', 'is_featured')



class ContractorSerializer(serializers.ModelSerializer):
    galleries = GallerySerializer(many= True, read_only= True)
    projects = ContractProjectListSerializer(many= True, read_only= True)
    description = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Contractor
        fields = ('id', 'name', 'galleries', 'description', 'projects', 'image_url')

    def get_description(self, obj):
        if not obj.description:
            return ""
        return str(obj.description)

    def get_image_url(self, obj):
        if obj.image_thumbnail:
            return obj.image_thumbnail.url
        if obj.image:
            return obj.image.url
        return None





class RegistrationContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationContractor
        fields = ('id', 'full_name', 'email', 'phone', 'contractor_type', 'is_checked', 'created')


