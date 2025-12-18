# investment/admin.py
from django.contrib import admin
from .models import Investment
from utils.admin import DateTimeAdminMixin



@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_fullname",
        "user_mobile",
        "project",
        "area",
        "base_amount",
        "total_payment",
        "status",
        "created",
    )

    list_filter = (
        "status",
        "project",
        "created",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__mobile_number",
        "project__title",
    )

    ordering = ("-created",)

    readonly_fields = (
        "user",
        "project",
        "area",
        "price_per_meter",
        "base_amount",
        "fee_amount",
        "tax_amount",
        "total_payment",
        "status",
        "created",
        "updated",
        *DateTimeAdminMixin.readonly_fields,
    )

    fieldsets = (
        ("اطلاعات کاربر", {
            "fields": ("user",)
        }),
        ("اطلاعات پروژه", {
            "fields": ("project", "area")
        }),
        ("جزئیات مالی", {
            "fields": (
                "price_per_meter",
                "base_amount",
                "fee_amount",
                "tax_amount",
                "total_payment",
            )
        }),
        ("وضعیت", {
            "fields": ("status",)
        }),
        ("زمان‌ها", {
            "fields": ("created", "updated")
        }),
        *DateTimeAdminMixin.fieldsets,
    )

    def user_fullname(self, obj):
        return obj.user.fullname if obj.user else "-"

    user_fullname.short_description = "نام کاربر"

    def user_mobile(self, obj):
        return obj.user.mobile_number if obj.user else "-"

    user_mobile.short_description = "شماره موبایل"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
