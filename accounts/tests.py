from .models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from .serializers import UserSerializer
from .serializers import LoginSerializer
from .views import createUser
from rest_framework import status


class CreateUserTests(APITestCase):
    def test_create_user(self):

        url = reverse('register')
        data = {"username": "Jardipotes", "email": "test@test.test", "first_name": "plante", "last_name": "ton voisin", "password": "SDZ1z3@Df", "has_garden": False,
                "bio": "lorem", "profile_image": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Jardipotes')

    def test_create_user_with_common_password(self):

        url = reverse('register')
        data = {"username": "common_password", "email": "test@test.test", "first_name": "plante", "last_name": "ton voisin", "password": "helloworld", "has_garden": False,
                "bio": "lorem", "profile_image": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_with_password_less_than_8_chars(self):

        url = reverse('register')
        data = {"username": "common_password", "email": "test@test.test", "first_name": "plante", "last_name": "ton voisin", "password": "ssss", "has_garden": False,
                "bio": "lorem", "profile_image": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class UserLoginTest(APITestCase):
    def test_user_login_with_random_element(self):
        url = reverse('login')
        data = {"email": "testinguser@test.test", "password": "SZsdqeeas123"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
