# Django Built-in
from django.contrib import admin

# Local
from utils.admin import DateTimeAdminMixin
from .models import SiteGlobalSetting


@admin.register(SiteGlobalSetting)
class SiteGlobalSettingAdmin(admin.ModelAdmin):
    list_display = ('address_short', 'created', 'updated',)
    fieldsets = (
        (None, {'fields': ('address', 'map',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)

    def address_short(self, obj):
        """نمایش خلاصه‌ای از آدرس برای لیست ادمین"""
        return obj.address[:50] + '...' if obj.address and len(obj.address) > 50 else obj.address
    address_short.short_description = "آدرس"

    def has_add_permission(self, request):
        """
        جلوگیری از ایجاد چند تنظیم مختلف.
        فقط اجازه می‌دهد یک رکورد تنظیمات وجود داشته باشد.
        """
        if SiteGlobalSetting.objects.exists():
            return False
        return True
