from django.contrib import admin
from .models import Category, FAQ


# -------------------------------
# Inline for FAQ inside Category
# -------------------------------
class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ('question', 'answer', 'is_featured')
    show_change_link = True


# -------------------------------
# Category Admin
# -------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'page_display_status',
        'created',
        'updated',
    )
    list_filter = ('page_display_status',)
    search_fields = ('name', 'slug')
    readonly_fields = ('created', 'updated')
    ordering = ('name',)

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'page_display_status')
        }),
        ('سئو', {
            'fields': (
                'search_engine_title',
                'search_engine_description',
                'search_engine_keywords',
                'canonical_link',
            )
        }),
        ('تاریخ', {
            'fields': ('created', 'updated')
        }),
    )

    # برای ساخت خودکار slug از name (اختیاری)
    prepopulated_fields = {"slug": ("name",)}


# -------------------------------
# Separate FAQ Admin (optional)
# -------------------------------
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_featured', 'created', 'updated')
    list_filter = ('category', 'is_featured')
    # list_editable = ('is_featured',)
    search_fields = ('question',)
    readonly_fields = ('created', 'updated')
    ordering = ('-created',)

    fieldsets = (
        (None, {
            'fields': ('category', 'question', 'answer', 'is_featured')
        }),
        ('تاریخ', {
            'fields': ('created', 'updated')
        }),
    )
