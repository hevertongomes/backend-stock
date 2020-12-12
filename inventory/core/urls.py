from django.urls import path
from .views import user_create, update_password, UserList, delete_user, get_question

urlpatterns = [
    path('users/', user_create, name='user-create'),
    path('newpassword/', update_password, name='new-password'),
    path('total_users/', UserList.as_view(), name='users'),
    path('delete_user/<str:username>', delete_user, name='delete-user'),
    path('get_question/', get_question, name='get-question')
]
