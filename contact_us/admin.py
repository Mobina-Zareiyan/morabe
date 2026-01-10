from django.contrib import admin

from utils.admin import DateTimeAdminMixin
from .models import ContactUsMessages


# Register your models here.

@admin.register(ContactUsMessages)
class ContactUsMessagesAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'is_checked', 'created',)
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'phone', 'message', 'is_checked',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    list_filter = ('is_checked',)
    list_editable = ('is_checked',)
    search_fields = ('full_name', 'email')
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    actions = ('change_checked_to_true', 'change_checked_to_false',)
#   این چجوری کار میکنه؟؟؟
    @admin.action(description='تغییر به بررسی شده')
    def change_checked_to_true(modeladmin, request, queryset):
        queryset.update(is_checked=True)

    @admin.action(description='تغییر به بررسی نشده')
    def change_checked_to_false(modeladmin, request, queryset):
        queryset.update(is_checked=False)
