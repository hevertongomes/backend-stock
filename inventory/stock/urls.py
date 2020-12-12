from django.urls import path
from .views import (
    StockItemList,
    StockList,
    StockDetail,
    StockItemDetail,
    add_stock_item,
    udpdate_stock_item,
    deactivate_stock_item,
    get_stock_items,
    add_stock
)

urlpatterns = [
    path('stocks/', StockList.as_view(), name='stocks'),
    path('stocks/<int:pk>/', StockDetail.as_view(), name='stock'),
    path('stocks-items/', StockItemList.as_view(), name='stock-items'),
    path('stocks-items/<int:pk>', StockItemDetail.as_view(), name='stock-item'),

    path('addstock/', add_stock, name='add_stock'),

    # item update qtd
    path('totalstocks/', get_stock_items, name='total-stocks'),
    path('additemstock/', add_stock_item, name='add-item-stock'),
    path('updateitemstock/<int:stock_item_id>', udpdate_stock_item, name='up-stock-tem'),
    path('deactivateitemstock/<int:stock_item_id>', deactivate_stock_item, name='deactivate-item-stock')
]
