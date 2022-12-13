from accounts.factories.user import UserFactory
from accounts.factories.garden import GardenFactory
from .models import User, Garden
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

"""
TODO: implement factory w / fake data to run more tests
"""


class CreateUserTests(APITestCase):
    def test_create_user(self):

        url = reverse("register")
        data = UserFactory.create_user(email="helloworld@test.test")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'helloworld@test.test')


class CreateGardenTests(APITestCase):
    def test_create_garden(self):

        url = reverse('create_garden')
        factoryUser = UserFactory.create_user()
        user = User.objects.create(**factoryUser)
        print(user)
        data = GardenFactory.create_garden(userId=user.id, title='au vert')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Garden.objects.count(), 1)
        self.assertNotEqual(Garden.objects.get().title, '')
