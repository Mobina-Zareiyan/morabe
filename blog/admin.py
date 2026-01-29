# Django Built-in Modules
from django.contrib import admin

# Local Apps
from utils.admin import DateTimeAdminMixin
from .models import Blog, BlogComment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')  # نمایش ستون‌ها در لیست
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'banner_description', 'full_description', 'newest_blog')
        }), *DateTimeAdminMixin.fieldsets,
    )
    search_fields = ('title', 'banner_description')  # جستجو روی عنوان و توضیح بنر
    list_filter = ('created', 'updated')
    filter_horizontal = ('newest_blog',)
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)

    def get_thumbnail_url(self, obj):
        return obj.get_image


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog', 'is_visible')
    list_filter = ('is_visible',)
    search_fields = ('name', 'email', 'content')
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
