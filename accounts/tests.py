from accounts.factories.user import UserFactory
from .models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

"""
TODO: implement factory w / fake data to run more tests
"""


class CreateUserTests(APITestCase):
    def test_create_user(self):

        url = reverse('register')
        data = UserFactory.create_user(email='helloworld@test.test')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'helloworld@test.test')
