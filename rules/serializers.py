# Local Apps
from .models import Rules

# Third Party Packages
from rest_framework import serializers


class RulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rules
        fields = ['id', 'title', 'description', 'created', 'updated']
