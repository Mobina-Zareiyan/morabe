from django.contrib import admin
from .models import Rules, RuleItem



# تعریف Inline برای RuleItem
class RuleItemInline(admin.TabularInline):
    model = RuleItem
    extra = 1  # تعداد فرم‌های خالی برای اضافه کردن سریع آیتم
    fields = ('order', 'topic', 'description')
    ordering = ('order',)

# تعریف Admin برای Rules
@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'page_display_status', 'created', 'updated')
    prepopulated_fields = {'slug': ('title',)}  # تولید خودکار slug از title
    inlines = [RuleItemInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'page_display_status')
        }),
        ('SEO', {
            'fields': ('search_engine_title', 'search_engine_description', 'search_engine_keywords', 'canonical_link')
        }),
    )

