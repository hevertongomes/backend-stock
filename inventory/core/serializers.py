from rest_framework import serializers
from .models import Question
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email','username', 'is_superuser']

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['question']