
from django.contrib import admin
from django.utils.html import format_html
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'parent', 'is_active', 'item_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    

    def item_count(self, obj):
        count = obj.active_items_count
        return format_html('<a href="?category__id__exact={}">{}</a>', obj.id, count)
    item_count.short_description = 'Active Items'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')# Register your models here.
