from rest_framework import serializers
from .models import RegistrationContractor, Gallery, Contractor
from project.serializers import ContractProjectListSerializer


class GallerySerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ReadOnlyField()

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'image_thumbnail', 'alt', 'title', 'subtitle')



class ContractorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'name', 'image', 'successful_project', 'work_experience', 'subtitle', 'is_featured')



class ContractorSerializer(serializers.ModelSerializer):
    galleries = GallerySerializer(many= True, read_only= True)
    projects = ContractProjectListSerializer(many= True, read_only= True)

    class Meta:
        model = Contractor
        fields = ('id', 'name', 'galleries', 'description', 'projects')




class RegistrationContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationContractor
        fields = ('id', 'full_name', 'email', 'phone', 'contractor_type', 'is_checked', 'created')


