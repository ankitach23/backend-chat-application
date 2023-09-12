from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ChatUser, Message
import logging
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if the username or email is already taken
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'error': 'Username or email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = ChatUser.objects.create(django_user=User.objects.create_user(username=username, email=email, password=password), online=False)

        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'message': 'User registered successfully.', 'access_token': access_token}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            # Generate JWT tokens


            # Login the user
            login(request, user)

            try:
                chat_user = ChatUser.objects.get(django_user=user)
                chat_user.online = True
                chat_user.save()
            except ChatUser.DoesNotExist:
                pass

            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')
        user = authenticate(request, username=username_or_email, password=password)
        chat_user = ChatUser.objects.get(django_user=user)
        

        # Set the user's online status to False
        chat_user.online = False
        chat_user.save()

        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_online_users(request):
    if request.method == 'GET':
        online_users = ChatUser.objects.filter(online=True)
        user_data = [{'id': user.id, 'username': user.django_user.username} for user in online_users]
        return Response(user_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def start_chat(request):
    if request.method == 'POST':
        recipient_id = request.data.get('recipient_id')
        sender_chatuser = request.user.chatuser  # Get the ChatUser associated with the User

        try:
            recipient = ChatUser.objects.get(id=recipient_id, online=True)
        except ChatUser.DoesNotExist:

            return Response({'error': 'Recipient is offline or does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Implement chat initiation logic here (e.g., create a new chat room, etc.)

        return Response({'message': 'Chat initiated successfully.'}, status=status.HTTP_201_CREATED)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['POST'])
def send_message(request):
    if request.method == 'POST':
        sender = request.user.chatuser
        recipient_id = request.data.get('recipient_id')
        content = request.data.get('content')

        try:
            recipient = ChatUser.objects.get(id=recipient_id)
        except ChatUser.DoesNotExist:
            return Response({'error': 'Recipient does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if not recipient.online:
            return Response({'error': 'Recipient is offline.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the message
        message = Message(sender=sender, receiver=recipient, content=content)
        message.save()

        # Use Django Channels to send the message in real-time
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{recipient_id}",
            {
                'type': 'chat.message',
                'message': content,
                'sender_id': sender.id,
                'recipient_id': recipient_id,
            }
        )

        return Response({'message': 'Message sent successfully.'}, status=status.HTTP_201_CREATED)


@require_GET
def suggested_friends(request, user_id):
    # Load user data from the JSON file
    with open('chatapp/constant/users.json', 'r') as json_file:
        user_data = json.load(json_file)

    # Find the user for the given user_id
    current_user = None
    for user in user_data.get('users', []):
        if user.get('id') == int(user_id):
            current_user = user
            break

    if not current_user:
        return JsonResponse({'error': 'User not found.'}, status=404)

    # Define a function to calculate a score for a user's compatibility with the current user
    def calculate_score(other_user):
        interests_weight = 0.4
        age_weight = 0.6

        interests_score = sum(
            (current_user['interests'].get(interest, 0) * other_user['interests'].get(interest, 0))
            for interest in current_user['interests']
        )

        age_score = 100 - abs(current_user['age'] - other_user['age'])

        return interests_weight * interests_score + age_weight * age_score

    # Calculate compatibility scores for all users
    compatibility_scores = [
        {
            'id': user['id'],
            'name': user['name'],
            'score': calculate_score(user)
        }
        for user in user_data.get('users', [])
        if user.get('id') != int(user_id)  # Exclude the current user
    ]

    # Sort users by compatibility score in descending order
    sorted_users = sorted(compatibility_scores, key=lambda x: x['score'], reverse=True)

    # Return the top 5 recommended friends
    recommended_friends = sorted_users[:5]

    return JsonResponse(recommended_friends, safe=False)