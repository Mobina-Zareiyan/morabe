# Django Built-in Modules
from django.contrib.auth.admin import Group
from django.contrib import admin

# Local Apps
from .models import User, OtpCode



admin.site.unregister(Group)


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
        'is_authenticate',
        'is_staff',
        'is_superuser'
    )

    # فیلدهای جستجو
    search_fields = ('mobile_number', 'first_name', 'last_name', 'national_code', 'referral_code')

    list_editable = ('is_active', )
    # فیلتر سمت راست
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'province', 'city')

    readonly_fields= ('qr_code_base64', 'seryal', 'video')

    # بخش‌بندی فرم
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'mobile_number', 'password')}),
        ('اطلاعات اضافی', {'fields': ('date_birth', 'national_code', 'province', 'city', 'address')}),
        ('معرف / کد معرف', {'fields': ('referral_code', 'referred_by', 'qr_code_base64',)}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'seryal', 'video', 'is_authenticate')}),
    )

    # مرتب سازی
    ordering = ('-created',)

    # اضافه کردن Inlineها
    inlines = (ReferralInline,)

    # نمایش تعداد زیرمجموعه‌ها
    def get_invited_count(self, obj):
        return obj.referrals.count()
    get_invited_count.short_description = 'تعداد زیرمجموعه‌ها'



    # # --------------------------------
    # # محدود کردن دسترسی حذف
    # # --------------------------------
    # def has_delete_permission(self, request, obj=None):
    #     # هیچ وقت اجازه حذف کاربر را نده
    #     return False
    #
    #
    # def get_readonly_fields(self, request, obj=None):
    #     ro_fields = list(self.readonly_fields)
    #     if not request.user.is_superuser:
    #         ro_fields += ['is_staff', 'is_superuser']
    #     return ro_fields



@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'is_active', 'is_verified', 'expires_at')
    readonly_fields = ('phone_number', 'code', 'is_active', 'is_verified', 'expires_at', )
