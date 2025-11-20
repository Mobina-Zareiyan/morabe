from rest_framework import generics
from .models import Blog
from .serializers import BlogListSerializer, BlogDetailSerializer, BlogCommentSerializer, BlogComment

class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer


class BlogDetailAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.prefetch_related(
        'newest_blog',
        'comments'
    )
    serializer_class = BlogDetailSerializer
    lookup_field = 'slug'


class BlogCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = BlogCommentSerializer
    queryset = BlogComment.objects.all()

    def perform_create(self, serializer):
        blog_id = self.request.data.get('blog')
        serializer.save(blog_id=blog_id)

