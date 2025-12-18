from django.contrib.auth.admin import Group
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import User
from seo.admin import AbstractBaseSeoModel, MetadataModel



admin.site.unregister(Group)

# -----------------------------
# Inline برای Metadata
# -----------------------------


# -----------------------------
# Inline برای زیرمجموعه‌ها (Referrals)
# -----------------------------
class ReferralInline(admin.TabularInline):
    model = User
    fk_name = 'referred_by'  # مشخص می‌کند این Inline مربوط به چه فیلدی است
    fields = ('first_name', 'last_name', 'mobile_number', 'referral_code', 'date_birth')
    readonly_fields = ('first_name', 'last_name', 'mobile_number', 'referral_code', 'date_birth')
    extra = 0
    can_delete = False
    verbose_name = 'زیرمجموعه'
    verbose_name_plural = 'زیرمجموعه‌ها'


# -----------------------------
# Admin کاربر
# -----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # ستون‌های لیست نمایش
    list_display = (
        'id',
        'mobile_number',
        'first_name',
        'last_name',
        'national_code',
        'date_birth',
        'referral_code',
        'get_invited_count',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    # فیلدهای جستجو
    search_fields = ('mobile_number', 'first_name', 'last_name', 'national_code', 'referral_code')

    # فیلتر سمت راست
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'province', 'city')

    # بخش‌بندی فرم
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'mobile_number', 'password')}),
        ('اطلاعات اضافی', {'fields': ('date_birth', 'national_code', 'province', 'city', 'address')}),
        ('معرف / کد معرف', {'fields': ('referral_code', 'referred_by')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # نمایش تعداد زیرمجموعه‌ها
    def get_invited_count(self, obj):
        return obj.referrals.count()
    get_invited_count.short_description = 'تعداد زیرمجموعه‌ها'

    # مرتب سازی
    ordering = ('-created',)

    # اضافه کردن Inlineها
    inlines = ( ReferralInline, )
