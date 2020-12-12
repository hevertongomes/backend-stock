from rest_framework import generics
from django_filters import rest_framework as filters
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from .models import Item
from .serializers import ItemSerializer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from datetime import datetime, timedelta
import json
from rest_framework import permissions
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ItemList(generics.ListAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['name']


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_item(request):
    now = datetime.now()
    user = request.user.username
    logger.info('Usuário '+ user +' Cadastrou um item na data ' + str(now))
    payload = json.loads(request.body)
    try:
        item = Item.objects.create(
            name=payload["name"],
            unit=payload["unit"],
            brand=payload["brand"],
            cost_value=payload["cost_value"],
            current_inventory=payload["current_inventory"],
            minimum_stock=payload["minimum_stock"],
            validaty=payload["validaty"],
        )
        serializer = ItemSerializer(item)
        return JsonResponse({'item': serializer.data}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def update_item(request, item_id):
    now = datetime.now()
    user = request.user.username
    logger.info('Usuário '+ user +' Atualizou um item na data ' + str(now))
    payload = json.loads(request.body)
    try:
        item = Item.objects.filter(id=item_id)
        item.update(**payload)
        up = Item.objects.get(id=item_id)
        serializer = ItemSerializer(up)
        return JsonResponse({'book': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def total_items(request):
    items = Item.objects.filter(active=True)
    serializer = ItemSerializer(items, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def item_stock_minimum(request):
    items = Item.objects.filter(active=True)
    minium_stocks = []
    for i in items:
        if i.current_inventory <= i.minimum_stock:
            minium_stocks.append(i)
    serializer = ItemSerializer(minium_stocks, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def item_expired(request):
    now = datetime.now()
    date_now = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    items = Item.objects.filter(validaty__lte=date_now, active=True)
    serializer = ItemSerializer(items, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def items_near_expires(request):
    now = datetime.now()
    date_now = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    now2 = datetime.now()
    now2 += timedelta(days=60)
    date_now2 = str(now2.year) + '-' + str(now2.month) + '-' + str(now2.day)
    items = Item.objects.filter(validaty__range=[date_now, date_now2], active=True)
    serializer = ItemSerializer(items, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def deactivate_item(request, item_id):
    now = datetime.now()
    user = request.user.username
    logger.info('Usuário '+ user +' Deletou um item na data ' + str(now))
    try:
        item = Item.objects.get(id=item_id)
        item.active = False
        item.save()
        serializer = ItemSerializer(item)
        return JsonResponse({'item': serializer.data}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

