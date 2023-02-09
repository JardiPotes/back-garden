from rest_framework.test import force_authenticate, APIClient, RequestsClient
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from .models import User
from .factory import UserFactory
from .views import AuthViewSet
import json


class TestRegisterUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john@snow.com', 'johnpassword')
        self.client.login(email='john@snow.com', password='johnpassword')

    def test_can_create_account(self):
        data = UserFactory.create_user_dict(email="hellothere@test.test")
        response = self.client.post('/api/auth/register', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(email="hellothere@test.test").exists(), True)

    def test_cannot_create_account_with_invalid_email(self):
        data = UserFactory.create_user_dict(email="lol.l")
        response = self.client.post('/api/auth/register', data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_response['email'], ["Enter a valid email address."])

    def test_cannot_create_user_with_already_existed_email(self):
        data = UserFactory.create_user_dict(email="john@snow.com")
        response = self.client.post('/api/auth/register', data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_response['email'], ["user with this email address already exists."])

    def test_cannot_create_user_with_password_less_than_8_chars(self):
        data = UserFactory.create_user_dict(password="123")
        response = self.client.post('/api/auth/register', data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_response['password'], ["This password is too short. It must contain at least 8 characters.", "This password is too common.", "This password is entirely numeric."])


class TestUserLogin(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john@snow.com', 'johnpassword')

    def test_can_login_with_valid_email_password(self):
        data = {"email": "john@snow.com", "password": "johnpassword"}
        response = self.client.post('/api/auth/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_login_with_invalid_email_or_password(self):
        data = {"email": "john@snow.com", "password": "123"}
        response = self.client.post('/api/auth/login', data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_response, ['Invalid email/password. Please try again!'])


class TestUserLogout(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john@snow.com', 'johnpassword')
        self.client.login(email='john@snow.com', password='johnpassword')

    def test_can_logout(self):
        data = {"email": "john@snow.com", "password": "johnpassword"}
        response = self.client.post('/api/auth/logout', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestListUsers(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john@snow.com', 'johnpassword')
        self.user = User.objects.create_user('hello@lol.fr', 'hellofoobar')

    def test_can_list_all_users(self):

        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)


class TestGetUserDetail(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john@snow.com', 'johnpassword')
        self.user = User.objects.create_user('hello@lol.fr', 'hellofoobar')

    def test_can_get_user_info_by_id(self):
        response = self.client.get('/api/users/1')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['id'], 1)
        self.assertEqual(json_response['email'], 'john@snow.com')


class TestResetPassword(APITestCase):
    def setUp(self):
        user = User.objects.create_user('hello@world', 'hello_world_123')
        self.client.force_authenticate(user=user)

    def test_can_reset_password_with_correct_credentials(self):
        data = {"current_password": "hello_world_123", "new_password": "new_hello_world_123"}
        response = self.client.post('/api/auth/password_change', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
