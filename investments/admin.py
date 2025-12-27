from django.contrib import admin
from .models import Investment, InvestmentSale
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
        "locked_area",
        "sold_area",
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






@admin.register(InvestmentSale)
class InvestmentSaleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "investment_info",
        "seller_fullname",
        "buyer_fullname",
        "selling_area",
        "sold_area",
        "price_per_meter",
        "base_amount",
        "total_payment",
        "status",
        "created",
    )

    list_filter = (
        "status",
        "investment__project",
        "created",
    )

    search_fields = (
        "investment__project__title",
        "seller__first_name",
        "seller__last_name",
        "seller__mobile_number",
        "buyer__first_name",
        "buyer__last_name",
        "buyer__mobile_number",
    )

    ordering = ("-created",)

    readonly_fields = (
        "investment",
        "seller",
        "buyer",
        "selling_area",
        "sold_area",
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
        ("اطلاعات فروش", {
            "fields": ("investment", "seller", "buyer")
        }),
        ("جزئیات متراژ", {
            "fields": ("selling_area", "sold_area", "price_per_meter")
        }),
        ("جزئیات مالی", {
            "fields": ("base_amount", "fee_amount", "tax_amount", "total_payment")
        }),
        ("وضعیت", {
            "fields": ("status",)
        }),
        ("زمان‌ها", {
            "fields": ("created", "updated")
        }),
        *DateTimeAdminMixin.fieldsets,
    )

    # نمایش اطلاعات سرمایه‌گذاری مرتبط
    def investment_info(self, obj):
        return f"{obj.investment} | پروژه: {obj.investment.project.title}"
    investment_info.short_description = "سرمایه‌گذاری"

    # نمایش نام فروشنده
    def seller_fullname(self, obj):
        return obj.seller.fullname if obj.seller else "-"
    seller_fullname.short_description = "فروشنده"

    # نمایش نام خریدار
    def buyer_fullname(self, obj):
        return obj.buyer.fullname if obj.buyer else "-"
    buyer_fullname.short_description = "خریدار"

    def has_add_permission(self, request):
        # جلوگیری از ایجاد دستی
        return False

    def has_delete_permission(self, request, obj=None):
        # جلوگیری از حذف دستی
        return False
