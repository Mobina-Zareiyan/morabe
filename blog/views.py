# Django Built-in Modules
from django.shortcuts import get_object_or_404

# Local Apps
from .models import Blog
from .serializers import BlogListSerializer, BlogDetailSerializer, BlogCommentSerializer, BlogComment

# Third Party Packages
from rest_framework import generics


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer


class BlogDetailAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.prefetch_related(
        'newest_blog',
        'comments'
    )
    serializer_class = BlogDetailSerializer
    lookup_field = 'id'


class BlogCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = BlogCommentSerializer
    queryset = BlogComment.objects.all()

    def perform_create(self, serializer):
        blog_id = self.kwargs['id']
        blog = get_object_or_404(Blog, pk= blog_id)
        serializer.save(blog= blog)

