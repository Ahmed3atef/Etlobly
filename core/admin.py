from django.contrib import admin
from .models import Restaurant, MenuItem, Menu, OrderRequest, OrderItem

class MenuItemInline(admin.TabularInline):
    model = Menu.menu_items.through
    extra = 1
    verbose_name = "Menu Item"
    verbose_name_plural = "Menu Items"

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]
    list_display = ['restaurant']
    exclude = ['menu_items']  # Exclude the ManyToManyField to hide the default field

# Register other models
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(OrderRequest)
admin.site.register(OrderItem)
