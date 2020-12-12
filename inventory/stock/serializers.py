from rest_framework import serializers
from .models import Stock, StockItem

class StockSerializer(serializers.ModelSerializer):

    class Meta:

        model = Stock
        fields = '__all__'


class StockItemSerializer(serializers.ModelSerializer):  
    
    item_name = serializers.SerializerMethodField(source='get_item_name')
    movement = serializers.SerializerMethodField(source="get_movement")

    class Meta:

        model = StockItem
        fields = (
            'active',
            'id',
            'stock',
            'item',
            'qtd',
            'item_name',
            'movement'
        )
    
    def get_item_name(self, obj):
        return obj.item.name
    
    def get_movement(self, obj):
        return obj.stock.get_movement_display()
    
