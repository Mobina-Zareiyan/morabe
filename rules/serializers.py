from rest_framework import serializers
from .models import Rules, RuleItem

class RuleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleItem
        fields = ['id', 'topic', 'description', 'order']

class RulesSerializer(serializers.ModelSerializer):
    items = RuleItemSerializer(many=True, read_only=True)  # فیلد related_name='items'

    class Meta:
        model = Rules
        fields = ['id', 'title', 'slug', 'page_display_status', 'created', 'updated', 'items']
