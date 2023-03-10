import json

from rest_framework.test import APITestCase

from accounts.factory import UserFactory
from apis.factory import GardenFactory, TestHelper

from .models import Garden, User


class TestCreateGarden(APITestCase):
    def test_can_create_garden_with_valid_attributes(self):

        user = UserFactory.create_user()
        data = GardenFactory.create_garden_dict(user_id=user.id, title="mylene")
        self.client.force_authenticate(user=user)

        response = self.client.post("/api/gardens", data, format="json")
        assert response.status_code == 201
        assert Garden.objects.count() == 1
        assert Garden.objects.get().title == "mylene"

    def test_cannot_create_garden_with_zipcode_too_long(self):

        user = UserFactory.create_user()
        data = GardenFactory.create_garden_dict(user_id=user.id, zipcode="469999")

        self.client.force_authenticate(user=user)
        response = self.client.post("/api/gardens", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["zipcode"] == [
            "Ensure this field has no more than 5 characters."
        ]

    def test_cannot_create_garden_with_too_long_title(self):

        random_string_more_than_hundred_char = (
            TestHelper.random_string_more_than_hundred_char(150)
        )
        user = UserFactory.create_user()
        data = GardenFactory.create_garden_dict(
            user_id=user.id, title=random_string_more_than_hundred_char
        )

        self.client.force_authenticate(user=user)
        response = self.client.post("/api/gardens", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["title"] == [
            "Ensure this field has no more than 100 characters."
        ]

    def test_cannot_create_garden_if_user_does_not_exist(self):
        data = GardenFactory.create_garden_dict(user_id="4")
        user = UserFactory.create_user()
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/gardens", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["user_id"] == ['Invalid pk "4" - object does not exist.']


class TestListGardens(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "hello@world", "hello_world_123", has_garden=True
        )
        self.user2 = User.objects.create_user(
            "hey@world.fr", "hekolololololo", has_garden=True
        )
        self.garden = Garden.objects.create(
            user_id=User(id=self.user.id), title="toto", zipcode="75001"
        )
        self.garden2 = Garden.objects.create(
            user_id=User(id=self.user2.id), title="tata", zipcode="93100"
        )
        self.garden3 = Garden.objects.create(
            user_id=User(id=self.user2.id), title="titi", zipcode="75001"
        )

    def test_should_list_all_gardens(self):
        response = self.client.get("/api/gardens")
        json_response = json.loads(response.content)
        res_list = []
        for res in json_response["results"]:
            res_list.append(res["user_id"])
        assert response.status_code == 200
        assert json_response["count"] == 3
        assert self.user.id in res_list
        assert self.user2.id in res_list

    def test_should_accept_filter_on_user_and_list_gardens(self):
        response = self.client.get("/api/gardens", {"user_id": self.user2.id})
        json_response = json.loads(response.content)
        user_id_list = []
        for res in json_response["results"]:
            user_id_list.append(res["user_id"])
        garden_id_list = []
        for res in json_response["results"]:
            garden_id_list.append(res["id"])

        assert response.status_code == 200
        assert json_response["count"] == 2
        assert self.user.id not in user_id_list
        assert self.garden.id not in garden_id_list

    def test_should_accept_filter_on_zipcode_and_list_gardens(self):
        response = self.client.get("/api/gardens", {"zipcode": "75001"})
        json_response = json.loads(response.content)
        zipcode_list = []
        for res in json_response["results"]:
            zipcode_list.append(res["zipcode"])
        assert response.status_code == 200
        assert json_response["count"] == 2
        assert "93100" not in zipcode_list


class TestUdateGarden(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "hello@world", "hello_world_123", has_garden=True
        )
        self.user2 = User.objects.create_user(
            "hey@world.fr", "hekolololololo", has_garden=True
        )
        self.garden = Garden.objects.create(
            user_id=User(id=self.user.id), title="toto", zipcode="75001"
        )

    def test_should_allow_to_update_if_user_is_the_owner(self):

        self.client.force_authenticate(user=self.user)
        data = {"title": "foobar"}
        response = self.client.patch(
            f"/api/gardens/{self.garden.id}", data, format="json"
        )
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response["title"] == data["title"]

    def test_should_not_allow_to_update_garden_if_auth_user_is_not_the_owner(self):

        self.user.refresh_from_db()
        self.client.force_authenticate(user=self.user2)
        data = {"title": "foobar"}
        response = self.client.put(
            f"/api/gardens/{self.garden.id}", data, format="json"
        )
        assert response.status_code == 403


class TestGardenPaginations(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "hello@world", "hello_world_123", has_garden=True
        )
        for i in range(12):
            self.garden = Garden.objects.create(user_id=User(self.user.id))

    def test_pagination_page_size_should_be_ten(self):
        response = self.client.get("/api/gardens")
        json_response = json.loads(response.content)
        assert json_response["count"] == 12
        assert len(json_response["results"]) == 10
        assert json_response["next"] is not None
