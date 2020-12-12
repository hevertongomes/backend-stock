from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from rest_framework import status
from .models import Question
import json
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def user_create(request):
    now = datetime.now()
    user = request.user.username
    logger.info('Usuário '+ user +' cadastrou um novo usuário ' + str(now))
    payload = json.loads(request.body)
    try:
        user = User.objects.create_user(
            payload['username'],
            payload['email'],
            payload['password']
        )
        if payload['admin'] == True:
            user.is_superuser = True
            user.is_staff = True
        user.first_name = payload['first_name']
        user.last_name = payload['last_name']
        user.save()

        question = Question.objects.create(
            user=user,
            question=payload['question'],
            answer=payload['answer']
        )
        print(question)
        
        return JsonResponse({'user': str(user)}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_password(request):
    payload = json.loads(request.body)
    try:
        user = User.objects.get(username__exact=payload['username'])
        q = Question.objects.get(user=user)

        if payload['answer'] == q.answer:
            user.set_password(payload['password'])
            user.save()
        else:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'user': str(user)}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def get_question(request):
    payload = json.loads(request.body)
    print(payload)
    try:
        user = User.objects.get(username__exact=payload['username'])
        q = Question.objects.get(user=user)
        print(user.email)
        print(q.question)
        if payload['email'] == user.email:
            return JsonResponse({'question': str(q.question)}, safe=True, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def delete_user(request, username):
    now = datetime.now()
    user = request.user.username
    try:
        u = User.objects.get(username = username)
        u.delete()
        logger.info('Usuário '+ user +' deletou o usuário ' + username + ' ' + str(now))
        return JsonResponse({'user': str(username)+' deletado com sucesso'}, safe=True, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo muito ruim deu errado'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
