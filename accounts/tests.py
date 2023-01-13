from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories.garden import GardenFactory
from accounts.factories.user import UserFactory

from .models import Garden, User

"""
TODO: implement factory w / fake data to run more tests
"""


class CreateUserTests(APITestCase):
    def test_create_user(self):

        url = reverse("register")
        data = UserFactory.create_user_dict(email="helloworld@test.test")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "helloworld@test.test")


class CreateGardenTests(APITestCase):
    def test_create_garden(self):

        url = reverse_lazy("gardens-list")
        user = UserFactory.create_user()
        data = GardenFactory.create_garden_dict(userId=user.id, title="au vert")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Garden.objects.count(), 1)
        self.assertNotEqual(Garden.objects.get().title, "")
