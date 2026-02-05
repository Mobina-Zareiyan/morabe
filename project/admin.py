# Django Built-in Modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.admin import DateTimeAdminMixin
from seo.admin import SeoAdminMixin
from unfold_admin.admin import ModelAdmin
from .models import (
    Project, ProjectStatus,
    Gallery, ProjectProgressReport,
    ProjectDocuments
)

# Third Party Packages
from unfold.admin import TabularInline




# ---------------------------------------------------------
# Inline Models
# ---------------------------------------------------------
class GalleryInline(TabularInline):
    model = Gallery
    extra = 1
    fields = ("image", "alt")
    verbose_name = _("تصویر")
    verbose_name_plural = _("گالری پروژه")


class ProjectProgressReportInline(TabularInline):
    model = ProjectProgressReport
    extra = 1
    verbose_name = _("گزارش")
    verbose_name_plural = _("گزارش‌های پیشرفت")


class ProjectDocumentsInline(TabularInline):
    model = ProjectDocuments
    extra = 1
    verbose_name = _("سند")
    verbose_name_plural = _("اسناد پروژه")


# ---------------------------------------------------------
# Project Admin
# ---------------------------------------------------------
@admin.register(Project)
class ProjectAdmin(SeoAdminMixin, ModelAdmin):
    list_display = (
        'title', 'province', 'city', 'usage_type', 'get_contractors', 'status', 'price_per_meter', 'created',
        'page_display_status', 'is_featured', 'remaining_area', 'sold_area',
    )

    list_filter = (
        'province',
        'city',
        'usage_type',
        'status',
        'contractors',
    )

    search_fields = ('title', 'address', 'contractors__name')

    readonly_fields = (
        *DateTimeAdminMixin.readonly_fields,
        *SeoAdminMixin.readonly_fields,
        'display_sold_area_readonly',
        'display_remaining_area_readonly',
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'contractors',
                'usage_type',
                'status',
                'is_featured',
            )
        }),

        (_('موقعیت'), {
            'fields': (
                'province',
                'city',
                'address',
                'map',
            )
        }),

        (_('متراژ و قیمت'), {
            'fields': (
                'price_per_meter',
                'total_area',
                'usable_area',
                'complete_area',
                'display_sold_area_readonly',
                'display_remaining_area_readonly',
            )
        }),

        (_('مشخصات فیزیکی'), {
            'fields': (
                'floor_count',
                'unit_count',
                'bedroom_count',
                'parking_count',
                'warehouse_count',
            )
        }),

        (_('زمان‌بندی'), {
            'fields': (
                'start_date',
                'estimated_completion_date',
            )
        }),

        (_('سود و سرمایه‌گذاری'), {
            'fields': (
                'profit_to_date',
                'invest_start_from',
                'total_budget',
                'current_funding',
                'investable_area',
            )
        }),

        (_('توضیحات'), {
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

    def display_sold_area_readonly(self, obj):
        return f"✅ متراژ فروخته شده: {obj.sold_area:,} متر"

    display_sold_area_readonly.short_description = _("متراژ فروخته شده")

    def display_remaining_area_readonly(self, obj):
        return f"⏳ متراژ باقیمانده: {obj.remaining_area:,} متر"

    display_remaining_area_readonly.short_description = _("متراژ باقیمانده")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # اینجا همه سازندگان پروژه‌ها را یکجا لود می‌کنه و جلوی N+1 می‌گیره
        return qs.prefetch_related('contractors')

    def get_contractors(self, obj):
        return ", ".join([c.name for c in obj.contractors.all()])

    get_contractors.short_description = _('سازندگان')



# ---------------------------------------------------------
# ProjectStatus Admin
# ---------------------------------------------------------
@admin.register(ProjectStatus)
class ProjectStatusAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

