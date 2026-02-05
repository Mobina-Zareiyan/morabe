# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# Local Apps
from .models import Province, City
from utils.admin import DateTimeAdminMixin
from unfold_admin.admin import ModelAdmin



@admin.register(Province)
class ProvinceAdmin(ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
        (
            _('طول و عرض جغرافیایی'),
            {'fields': ('longitude', 'latitude',)}
        ),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(ModelAdmin):
    fieldsets = (
        (None, {'fields': ('province', 'name',)}),
        (
            _('طول و عرض جغرافیایی'),
            {'fields': ('longitude', 'latitude',)}
        ),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('province', 'name',)
    list_select_related = ('province',)
    list_filter = ('province',)
    search_fields = ('name',)
    autocomplete_fields = ('province',)



