from .models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from .serializers import UserSerializer
from .views import create_user, user_login
from rest_framework import status

"""
TODO: implement factory w / fake data to run more tests
"""


class CreateUserTests(APITestCase):
    def test_create_user(self):

        url = reverse('register')
        data = {"email": "helloworld@test.test", "first_name": "plante", "last_name": "ton voisin", "password": "SDZ1z3@Df", "has_garden": False,
                "bio": "lorem", "profile_image": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'helloworld@test.test')
