from .models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from .serializers import UserSerializer
from rest_framework import status


class UserTests(APITestCase):
    def test_create_user(self):

        url = reverse('register')
        data = {"username": "Jardipotes", "email": "test@test.test", "first_name": "plante", "last_name": "ton voisin", "password": "blablablablabla", "has_garden": False,
                "bio": "lorem", "profile_image": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Jardipotes')

    def test_list_user(self):
        url = reverse('users')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
