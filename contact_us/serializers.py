from rest_framework import serializers
from .models import ContactUsMessages

class ContactUsMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsMessages
        fields = ['id', 'full_name', 'email', 'phone', 'message', 'is_checked', 'created', 'updated']
        read_only_fields = ['id', 'is_checked', 'created', 'updated']
