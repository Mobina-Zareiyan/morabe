from django.contrib import admin

from utils.admin import DateTimeAdminMixin
from seo.admin import SeoAdminMixin        # اگر چنین میکسی نداری بگو تا برات بسازم
from .models import (
    Project, ProjectStatus,
    Gallery, ProjectProgressReport,
    ProjectDocuments
)


# ---------------------------------------------------------
# Inline Models
# ---------------------------------------------------------

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    fields = ("image", "alt")
    verbose_name = "تصویر"
    verbose_name_plural = "گالری پروژه"


class ProjectProgressReportInline(admin.TabularInline):
    model = ProjectProgressReport
    extra = 1
    verbose_name = "گزارش"
    verbose_name_plural = "گزارش‌های پیشرفت"


class ProjectDocumentsInline(admin.TabularInline):
    model = ProjectDocuments
    extra = 1
    verbose_name = "سند"
    verbose_name_plural = "اسناد پروژه"


# ---------------------------------------------------------
# Project Admin
# ---------------------------------------------------------

@admin.register(Project)
class ProjectAdmin(SeoAdminMixin, admin.ModelAdmin):
    list_display = (
        'title', 'province', 'city', 'usage_type',
        'contractor', 'status', 'price_per_meter',
        'created',  # از AbstractDateTimeModel
        'page_display_status',
    )

    list_filter = (
        'province',
        'city',
        'usage_type',
        'status',
        'contractor',
    )

    search_fields = ('title', 'address', 'contractor__name')

    readonly_fields = (
        *DateTimeAdminMixin.readonly_fields,
        *SeoAdminMixin.readonly_fields,
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'contractor',
                'usage_type',
                'status',
            )
        }),

        ('موقعیت', {
            'fields': (
                'province',
                'city',
                'address',
                'map',
            )
        }),

        ('متراژ و قیمت', {
            'fields': (
                'price_per_meter',
                'total_area',
                'usable_area',
                'complete_area',
            )
        }),

        ('مشخصات فیزیکی', {
            'fields': (
                'floor_count',
                'unit_count',
                'bedroom_count',
                'parking_count',
                'warehouse_count',
            )
        }),

        ('زمان‌بندی', {
            'fields': (
                'start_date',
                'estimated_completion_date',
            )
        }),

        ('سود و سرمایه‌گذاری', {
            'fields': (
                'profit_to_date',
                'invest_start_from',
            )
        }),

        ('توضیحات', {
            'fields': ('project_details',)
        }),

        *SeoAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets,
    )

    prepopulated_fields = {"slug": ("title",)}

    inlines = [
        GalleryInline,
        ProjectProgressReportInline,
        ProjectDocumentsInline,
    ]


# ---------------------------------------------------------
# ProjectStatus Admin
# ---------------------------------------------------------

@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

