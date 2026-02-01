# Local Apps
from .models import Category, FAQ

# Third Party Packages
from rest_framework import serializers



# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ["id", "name", "slug", "page_display_status"]
#
#
# class FAQSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#
#     class Meta:
#         model = FAQ
#         fields = ["id", "category", "question", "answer", "is_featured"]
#


class FAQInCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'category', "question", "answer", "is_featured"]


class CategoryWithFAQSerializer(serializers.ModelSerializer):
    faqs = FAQInCategorySerializer(many= True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'faqs']


