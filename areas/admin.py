# Django Built-in modules
from django.contrib import admin

# Local apps
from .models import Province, City
from utils.admin import DateTimeAdminMixin



@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('طول و عرض جغرافیایی', {'fields': ('longitude', 'latitude',)}),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('province', 'name',)}),
        ('طول و عرض جغرافیایی', {'fields': ('longitude', 'latitude',)}),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('province', 'name',)
    list_select_related = ('province',)
    list_filter = ('province',)
    search_fields = ('name',)
    autocomplete_fields = ('province',)



