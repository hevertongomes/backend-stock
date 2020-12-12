from django.urls import path
from .views import (
  ItemList,
  item_stock_minimum,
  item_expired,
  items_near_expires,
  total_items,
  deactivate_item,
  add_item,
  update_item
)

urlpatterns = [
    path('items/', ItemList.as_view(), name='items'),
    path('items/<int:item_id>', update_item, name='update-item'),
    path('add_item/', add_item, name='add-item'),
    
    path('items_minimum_stock/', item_stock_minimum, name='item-minimum'),
    path('items_total/', total_items,  name='items-total'),
    path('items_expired/', item_expired, name='item_expired'),
    path('items_near_expires/', items_near_expires, name='item_near_expires'),

    path('item_deactivate/<int:item_id>', deactivate_item, name='deactivate-item')
]
