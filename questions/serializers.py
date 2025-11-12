from rest_framework import serializers
from .models import Category, FAQ


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "page_display_status",
            "search_engine_title",
            "search_engine_description",
            "search_engine_keywords",
            "canonical_link",
            "created",
            "updated",
        ]


class FAQSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )

    class Meta:
        model = FAQ
        fields = [
            "id",
            "category",
            "question",
            "answer",
            "is_featured",
            "created",
            "updated",
        ]
