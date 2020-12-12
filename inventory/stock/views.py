from .models import StockItem, Stock
from inventory.items.models import Item
from .serializers import StockSerializer, StockItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import generics, status
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class StockList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockItemList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer


class StockItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_stock_items(request):
    stock_items = StockItem.objects.filter(active=True)
    serializer = StockItemSerializer(stock_items, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def add_stock_item(request):
    now = datetime.now()
    user = request.user.username
    payload = json.loads(request.body)
    try:
        item = Item.objects.get(id=payload["item"])
        stock = Stock.objects.get(id=payload["stock"])
        item_stock = StockItem.objects.create(
            stock = stock,
            item = item,
            qtd = payload["qtd"]
        )
        
        if stock.movement == "0":
            item.current_inventory = float(item.current_inventory) + float(item_stock.qtd)
        else:
            item.current_inventory = float(item.current_inventory) - float(item_stock.qtd)
        item.save()
        print(stock)
        logger.info('Usuário '+ user +' adicinou o item '  + item.name + ' ao estoque ' + str(stock) + ' ' + str(now))
        serializer = StockItemSerializer(item_stock)
        return JsonResponse({'item_stock': serializer.data}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_stock(request):
    now = datetime.now()
    user = request.user.username
    payload = json.loads(request.body)
    try:
        stock = Stock.objects.create(
            nf=payload['nf'],
            movement=payload['movement']
        )
        logger.info('Usuário '+ user +' adicionou o estoque '  + stock.nf + ' ao banco ' + str(now))
        serializer = StockSerializer(stock)
        return JsonResponse({'item_stock': serializer.data}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def udpdate_stock_item(request, stock_item_id):
    payload = json.loads(request.body)
    try:
        item = Item.objects.get(id=payload["item"])
        stock = Stock.objects.get(id=payload["stock"])
        stock_item_i = StockItem.objects.filter(id=stock_item_id)
        stock_item_i.update(
            stock = stock,
            item = item,
            qtd = payload["qtd"]
        )
        stock_item = StockItem.objects.get(id=stock_item_id)
        if stock.movement == "0":
            item.current_inventory = item.current_inventory + stock_item.qtd
        else:
            item.current_inventory = item.current_inventory - stock_item.qtd
        item.save()   
        serializer = StockItemSerializer(stock_item)
        return JsonResponse({'stock_item': serializer.data}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def deactivate_stock_item(request, stock_item_id):
    now = datetime.now()
    user = request.user.username
    try:
        stock_item = StockItem.objects.get(id=stock_item_id)
        print()
        item = Item.objects.get(id=stock_item.item.id)
        stock = Stock.objects.get(id=stock_item.stock.id)
        stock_item.active = False
        stock_item.save()
        if stock.movement == "0":
            print('entrou')
            item.current_inventory = item.current_inventory - stock_item.qtd
        else:
            item.current_inventory = item.current_inventory + stock_item.qtd
        item.save()
        logger.info('Usuário '+ user +' deleletou o item '  + item.name + ' do estoque ' + str(stock) + ' ' + str(now))
        serializer = StockItemSerializer(stock_item)
        return JsonResponse({'stock_item': serializer.data}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
