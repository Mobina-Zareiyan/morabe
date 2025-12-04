from django.contrib import admin
from .models import Contractor, Gallery, RegistrationContractor

# ---------------------------------------------------------
# Inline Models
# ---------------------------------------------------------
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    fields = ("image_preview", "image", "title", "subtitle", "alt")
    readonly_fields = ("image_preview",)
    verbose_name = "تصویر"
    verbose_name_plural = "گالری‌ها"

    def image_preview(self, obj):
        if obj.image_thumbnail:
            return f'<img src="{obj.image_thumbnail.url}" width="150" height="84" />'
        return "-"
    image_preview.short_description = "پیش‌نمایش"
    image_preview.allow_tags = True


# ---------------------------------------------------------
# Contractor Admin
# ---------------------------------------------------------
@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
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
    readonly_fields = ("image_preview",)
    ordering = ("name",)
    inlines = [GalleryInline]

    fieldsets = (
        (None, {
            "fields": ("name", "subtitle", "description", "is_featured")
        }),
        ("تصویر", {
            "fields": ("image", "alt", "image_preview")
        }),
    )

    prepopulated_fields = {"slug": ("name",)} if hasattr(Contractor, "slug") else {}

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
    mark_as_checked.short_description = "علامت زدن به عنوان بررسی شده"
