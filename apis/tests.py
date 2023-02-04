from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from apis.factory import GardenFactory
from accounts.factory import UserFactory

from .models import Garden, User

"""
TODO: implement factory w / fake data to run more tests
"""


class CreateGardenTests(APITestCase):
    def test_create_garden(self):

        url = reverse_lazy("gardens-list")
        user = UserFactory.create_user()
        data = GardenFactory.create_garden_dict(user_id=user.id, title="au vert")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Garden.objects.count(), 1)
        self.assertNotEqual(Garden.objects.get().title, "")
