from rest_framework import serializers
from .models import Blog, BlogComment

class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ('id', 'name', 'email', 'content', 'created')
        read_only_fields = ('id', 'created')

class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'banner_description', 'get_image')  # لیست بلاگ‌ها

class BlogDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    newest_blog = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            'id', 'title', 'full_description',
            'created', 'get_image', 'newest_blog', 'comments'
        )

    def get_comments(self, obj):
        visible_comment = obj.comments.filter(is_visible= True)
        return BlogCommentSerializer(visible_comment, many= True).data

    def get_newest_blog(self, obj):
        return [{
            'id': b.id,
            'title': b.title,
            'get_image': b.get_image,
            'created': b.created,
        } for b in obj.newest_blog.all()]
