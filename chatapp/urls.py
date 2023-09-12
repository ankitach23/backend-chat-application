from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('online-users/', views.get_online_users, name='get_online_users'),
    path('chat/start/', views.start_chat, name='start_chat'),
    path('chat/send/', views.send_message, name='send_message'),
    path('suggested-friends/<int:user_id>/', views.suggested_friends, name='suggested_friends'),
    path('logout/', views.user_logout, name='user_logout')



    # Define other API endpoints as needed for chat functionality
]
