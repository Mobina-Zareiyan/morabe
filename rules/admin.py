from django.contrib import admin
from .models import Rules
from utils.admin import DateTimeAdminMixin



# تعریف Admin برای Rules
@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }), *DateTimeAdminMixin.fieldsets
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)


