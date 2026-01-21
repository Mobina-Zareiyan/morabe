from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Contractor, Gallery, RegistrationContractor
from seo.admin import SeoAdminMixin
from utils.admin import DateTimeAdminMixin


# ---------------------------------------------------------
# Inline Models
# ---------------------------------------------------------
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    fields = ("image_preview", "image", "title", "subtitle", "alt")
    readonly_fields = ("image_preview",)
    verbose_name = _("تصویر")
    verbose_name_plural = _("گالری‌ها")

    def image_preview(self, obj):
        if obj.image_thumbnail:
            return f'<img src="{obj.image_thumbnail.url}" width="150" height="84" />'
        return "-"
    image_preview.short_description = _("پیش‌نمایش")
    image_preview.allow_tags = True


# ---------------------------------------------------------
# Contractor Admin
# ---------------------------------------------------------
@admin.register(Contractor)
class ContractorAdmin(SeoAdminMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "is_featured",
        "successful_project",
        "work_experience",
        "image_preview"
    )
    list_editable = ("is_featured",)
    list_filter = ("is_featured",)
    search_fields = ("name", "subtitle", "description")
    readonly_fields = (
        "image_preview",
        *DateTimeAdminMixin.readonly_fields,
        *SeoAdminMixin.readonly_fields
    )
    ordering = ("name",)
    inlines = [GalleryInline]

    fieldsets = (
        (None, {
            "fields": ("name", "subtitle", "description", "successful_project", "work_experience", "is_featured",)
        }),
        (_("تصویر"), {
            "fields": ("image", "alt", "image_preview")
        }),
        *SeoAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets
    )

    prepopulated_fields = {"slug": ("name",)}

    def image_preview(self, obj):
        if obj.image_thumbnail:
            return f'<img src="{obj.image_thumbnail.url}" width="100" height="100" />'
        return "-"
    image_preview.short_description = "تصویر"
    image_preview.allow_tags = True


# ---------------------------------------------------------
# RegistrationContractor Admin
# ---------------------------------------------------------
@admin.register(RegistrationContractor)
class RegistrationContractorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "contractor_type", "is_checked", "created")
    list_filter = ("is_checked",)
    search_fields = ("full_name", "phone", "email", "contractor_type")
    readonly_fields = ("created",)
    ordering = ("-created",)
    actions = ["mark_as_checked"]

    def mark_as_checked(self, request, queryset):
        updated = queryset.update(is_checked=True)
        self.message_user(request, f"{updated} درخواست بررسی شد.")
    mark_as_checked.short_description = _("علامت زدن به عنوان بررسی شده")
