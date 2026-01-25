from rest_framework import serializers
from .models import Rules


class RulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rules
        fields = ['id', 'title', 'description', 'created', 'updated']
