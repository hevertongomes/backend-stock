from django.contrib import admin

from inventory.items.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'brand', 'cost_value','current_inventory', 'minimum_stock', 'validaty', 'active')
