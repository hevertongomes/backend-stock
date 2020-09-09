from django.contrib import admin

from inventory.stock.models import Stock, StockItem


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('nf', 'movement', 'active')


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('stock', 'item', 'qtd')

