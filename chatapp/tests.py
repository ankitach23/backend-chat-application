
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase,APILiveServerTestCase
from .models import ChatUser, Message
import json
from channels.testing import WebsocketCommunicator
from django.test import override_settings  # Import override_settings decorator
from asgiref.testing import ApplicationCommunicator  # Import ApplicationCommunicator
from asgiref.sync import sync_to_async
from django.test import TestCase
from channels.testing import ChannelsLiveServerTestCase
from channels.db import database_sync_to_async
class SuggestedFriendsAPITest(APITestCase):
    def test_suggested_friends(self):
        # Create a user and ensure the API returns suggested friends
        user = ChatUser.objects.create(django_user=User.objects.create_user('testuser', 'test@example.com', 'testpassword'))
        url = reverse('suggested_friends', args=[2])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        self.assertEqual(len(data), 5)  # Assuming the JSON file contains at least 5 users

    def test_suggested_friends_nonexistent_user(self):
        # Ensure the API returns an error for a nonexistent user
        url = reverse('suggested_friends', args=[9999])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
class UserRegistrationAPITest(APITestCase):
    def test_user_registration(self):
        url = reverse('user_register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_duplicate(self):
        url = reverse('user_register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}
        User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

    def test_user_login(self):
        url = reverse('user_login')
        data = {'username_or_email': 'testuser', 'password': 'testpassword'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid(self):
        url = reverse('user_login')
        data = {'username_or_email': 'testuser', 'password': 'wrongpassword'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetOnlineUsersAPITest(APITestCase):
    def test_get_online_users(self):
        # Create a user and mark them as online
        user = ChatUser.objects.create(django_user=User.objects.create_user('testuser', 'test@example.com', 'testpassword'), online=True)

        url = reverse('get_online_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_get_online_users_empty(self):
        # Ensure the API returns an empty list when no users are online
        url = reverse('get_online_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class StartChatAPITest(APITestCase):
    def setUp(self):
        # Create two users, one online and one offline
        self.sender = ChatUser.objects.create(django_user=User.objects.create_user('senderuser', 'sender@example.com', 'senderpassword'), online=True)
        self.offlinerecipient = ChatUser.objects.create(django_user=User.objects.create_user('offlinerecipientuser', 'recipient@example.com', 'recipientpassword'), online=False)
        self.onlinerecipient=ChatUser.objects.create(django_user=User.objects.create_user('onlinerecipientuser', 'recipient@example.com', 'recipientpassword'), online=True)


    def test_start_chat_with_online_recipient(self):
        url = reverse('start_chat')
        data = {'recipient_id': self.onlinerecipient.id}
        self.client.force_authenticate(user=self.sender.django_user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_start_chat_with_offline_recipient(self):
        # Ensure an error response is returned when starting a chat with an offline recipient
        url = reverse('start_chat')
        data = {'recipient_id': self.offlinerecipient.id}
        self.client.force_authenticate(user=self.sender.django_user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class SendMessageAPITest(APITestCase):
    def setUp(self):
        # Create two users, one online and one offline
        self.sender = ChatUser.objects.create(django_user=User.objects.create_user('senderuser', 'sender@example.com', 'senderpassword'), online=True)
        self.onlinerecipient = ChatUser.objects.create(django_user=User.objects.create_user('onlinerecipientuser', 'recipient@example.com', 'recipientpassword'), online=True)
        self.offlinerecipient = ChatUser.objects.create(django_user=User.objects.create_user('offlinerecipientuser', 'recipient@example.com', 'recipientpassword'), online=False)

    def test_send_message_online_recipient(self):
        url = reverse('send_message')
        data = {'recipient_id': self.onlinerecipient.id, 'content': 'Hello, recipient!'}  # Use self.recipient.id
        self.client.force_authenticate(user=self.sender.django_user)
    
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_send_message_offline_recipient(self):
        # Ensure an error response is returned when the recipient is offline
        url = reverse('send_message')
        data = {'recipient_id': self.offlinerecipient.id, 'content': 'Hello, recipient!'}
        self.client.force_authenticate(user=self.sender.django_user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

