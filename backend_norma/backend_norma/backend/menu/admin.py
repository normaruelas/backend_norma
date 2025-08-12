from django.contrib import admin
from .models import Category, Variant, Size, MenuItem, Price, Settings

class PriceInline(admin.TabularInline):
    model = Price
    extra = 0

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('public_id', 'name', 'category', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    inlines = [PriceInline]

admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(Size)
admin.site.register(Settings)
