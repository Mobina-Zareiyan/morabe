from rest_framework import serializers
from .models import Blog, BlogComment

class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ('id', 'name', 'email', 'content', 'created')  # فقط اطلاعاتی که فرانت نیاز دارد
        read_only_fields = ('id', 'created')

class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'banner_description', 'get_image')  # لیست بلاگ‌ها

class BlogDetailSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(many=True, read_only=True)

    newest_blog = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            'id', 'title', 'full_description',
            'created', 'get_image', 'newest_blog', 'comments'
        )

    def get_newest_blog(self, obj):
        return [{
            'id': b.id,
            'title': b.title,
            'get_image': b.get_image,
            'created': b.created,
        } for b in obj.newest_blog.all()]
