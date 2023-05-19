import json

from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.factory import UserFactory
from accounts.utils import temporary_image
from apis.factory import GardenFactory, TestHelper

from .models import Comment, Conversation, Garden, Message, Photo, User


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


class TestLeavingComments(APITestCase):
    def test_should_allow_a_user_to_comment_on_another(self):
        user = UserFactory.create_user()
        user2 = UserFactory.create_user()
        self.client.force_authenticate(user=user)
        data = {"author_id": user.id, "receiver_id": user2.id, "content": "coucou"}

        response = self.client.post("/api/comments", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 201
        assert json_response["author_id"] == user.id
        assert json_response["receiver_id"] == user2.id
        assert json_response["content"] == data["content"]

    def test_with_unauthenticated_user_should_fail(self):
        user = UserFactory.create_user()
        user2 = UserFactory.create_user()
        data = {"author_id": user.id, "receiver_id": user2.id, "content": "Hello"}

        response = self.client.post("/api/comments", data, format="json")
        assert response.status_code == 401


class TestFetchCommentsOfAGivenUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hello@world", "hello_world_123")
        self.user2 = User.objects.create_user("foo@bar.lol", "foobarlol")
        self.comment = Comment.objects.create(
            receiver_id=User(id=self.user.id), author_id=User(id=self.user2.id)
        )
        self.comment2 = Comment.objects.create(
            receiver_id=User(id=self.user2.id), author_id=User(id=self.user.id)
        )

    def test_should_fetch_author_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/comments?receiver_id={self.user.id}")
        json_response = json.loads(response.content)
        receiver_id_list = []
        for res in json_response["results"]:
            receiver_id_list.append(res["id"])

        author_list = []
        for res in json_response["results"]:
            author_list.append(res["author"])
        author = author_list[0]

        assert response.status_code == 200
        assert json_response["count"] == 1
        assert self.user2.id not in receiver_id_list
        assert author["id"] == self.user2.id
        assert author["experience"] == self.user2.experience
        assert author["profile_image"] is not None

    def test_should_return_empty_list_if_no_comments_for_the_given_user(self):
        user = UserFactory.create_user()
        self.client.force_authenticate(user=user)
        response = self.client.get(f"/api/comments?receiver_id={user.id}")
        json_response = json.loads(response.content)
        assert json_response["results"] == []


class TestUploadGardenPhotos(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.garden = Garden.objects.create(
            user_id=User(id=self.user.id), title="toto", zipcode="75001"
        )

    def test_with_authenticated_garden_owner_should_accept_one_image_upload(self):
        self.client.force_authenticate(user=self.user)
        data = {"garden_id": self.garden.id, "image": temporary_image()}
        response = self.client.post("/api/photos", data=data)
        json_response = json.loads(response.content)
        assert response.status_code == 201
        assert json_response["garden_id"] == self.garden.id
        assert json_response["image"] is not None

    def test_with_authenticated_garden_owner_should_accept_multiphle_images_upload_separately(
        self,
    ):
        self.client.force_authenticate(user=self.user)
        data = {"garden_id": self.garden.id, "image": temporary_image()}
        response = self.client.post("/api/photos", data=data)
        json_response = json.loads(response.content)
        assert response.status_code == 201
        assert json_response["garden_id"] == self.garden.id
        assert json_response["image"] is not None

        second_data = {"garden_id": self.garden.id, "image": temporary_image()}
        second_response = self.client.post("/api/photos", data=second_data)
        second_json_response = json.loads(response.content)
        assert second_response.status_code == 201
        assert second_json_response["garden_id"] == self.garden.id
        assert second_json_response["image"] is not None
        garden_photos = Photo.objects.filter(garden_id=self.garden.id)
        assert garden_photos.count() == 2

    def test_should_not_allow_non_garden_owner_to_upload_photos(self):
        not_owner = UserFactory.create_user()
        self.client.force_authenticate(user=not_owner)
        data = {"garden_id": self.garden.id, "image": temporary_image()}
        response = self.client.post("/api/photos", data=data)
        assert response.status_code == 403

    def test_should_return_401_for_unauthenticated_owner(self):
        data = {"garden_id": self.garden.id, "image": temporary_image()}
        response = self.client.post("/api/photos", data=data)
        assert response.status_code == 401


class TestListPhotos(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.garden = Garden.objects.create(
            user_id=User(id=self.user.id), title="toto", zipcode="75001"
        )

        self.user2 = User.objects.create_user("hola@world.fr", "hekolololololo")

        self.garden2 = Garden.objects.create(
            user_id=User(id=self.user2.id), title="toto", zipcode="75001"
        )
        self.client.force_authenticate(user=self.user)
        data = {"garden_id": self.garden.id, "image": temporary_image()}
        self.client.post("/api/photos", data=data)

        self.client.force_authenticate(user=self.user2)
        data2 = {"garden_id": self.garden2.id, "image": temporary_image()}
        self.client.post("/api/photos", data=data2)

    def test_should_list_all_garden_photos(self):
        response = self.client.get("/api/photos")
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response["count"] == 2

        garden_id_list = []
        for value in json_response["results"]:
            garden_id_list.append(value["garden_id"])
        assert self.garden.id in garden_id_list
        assert self.garden2.id in garden_id_list

    def test_should_accept_garden_id_as_params_and_list_all_photos(self):
        response = self.client.get(f"/api/photos?garden_id={self.garden.id}")
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response["count"] == 1

        garden_id_list = []
        for value in json_response["results"]:
            garden_id_list.append(value["garden_id"])

        assert self.garden.id in garden_id_list
        assert self.garden2.id not in garden_id_list


class TestUpdatePhotos(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.garden = Garden.objects.create(
            user_id=User(id=self.user.id), title="toto", zipcode="75001"
        )

        self.user2 = User.objects.create_user("hola@world.fr", "hekolololololo")

        self.garden2 = Garden.objects.create(
            user_id=User(id=self.user2.id), title="toto", zipcode="75001"
        )
        self.client.force_authenticate(user=self.user)
        data = {"garden_id": self.garden.id, "image": temporary_image()}
        self.client.post("/api/photos", data=data)

        self.client.force_authenticate(user=self.user2)
        data2 = {"garden_id": self.garden2.id, "image": temporary_image()}
        self.client.post("/api/photos", data=data2)

    def test_should_allow_to_update_the_garden_photo_for_the_owner(self):
        self.client.force_authenticate(user=self.user)
        photo = Photo.objects.get(garden_id=self.garden.id)
        photo_id = photo.id
        is_main_photo = photo.is_main_photo
        season = photo.season
        data = {"garden_id": self.garden.id, "season": 3, "is_main_photo": True}
        response = self.client.put(f"/api/photos/{photo_id}", data=data)
        json_response = json.loads(response.content)

        assert response.status_code == 200
        assert json_response["is_main_photo"] != is_main_photo
        assert json_response["season"] != season
        assert json_response["is_main_photo"] == data["is_main_photo"]
        assert json_response["season"] == data["season"]

    def test_should_return_403_if_not_garden_owner(self):
        self.client.force_authenticate(user=self.user)

        photo = Photo.objects.get(garden_id=self.garden2.id)

        data = {"garden_id": self.garden2.id, "season": 3, "is_main_photo": True}
        response = self.client.put(f"/api/photos/{photo.id}", data=data)
        assert response.status_code == 403


class TestLeavePrivateMessages(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.user2 = User.objects.create_user("hola@world.fr", "hekolololololo")
        self.conversation = Conversation.objects.create(
            chat_sender_id=self.user, chat_receiver_id=self.user2
        )
        self.message = Message.objects.create(
            sender_id=self.user,
            content="Hello there",
            conversation_id=self.conversation,
            sent_at=timezone.now() - timezone.timedelta(hours=1),
        )
        self.message2 = Message.objects.create(
            sender_id=self.user,
            content="Latest msg",
            conversation_id=self.conversation,
            sent_at=timezone.now(),
        )

    def test_should_return_401_if_not_authenticated(self):
        response = self.client.get("/api/conversations")
        assert response.status_code == 401

    def test_should_return_the_latest_message_of_conversation(self):
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/conversations")
        json_response = json.loads(response.content)
        assert response.status_code == 200
        latest_message_list = []
        for result in json_response["results"]:
            latest_message = result["latest_message"]["content"]
            latest_message_list.append(latest_message)
        assert self.message2.content in latest_message_list
        assert self.message.content not in latest_message_list

    def test_should_list_all_conversations_with_latest_message(self):
        self.conversation2 = Conversation.objects.create(
            chat_sender_id=self.user2, chat_receiver_id=self.user
        )
        self.message3 = Message.objects.create(
            sender_id=self.user2,
            content="Another msg",
            conversation_id=self.conversation2,
        )
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/conversations")
        json_response = json.loads(response.content)
        latest_message_list = []
        for result in json_response["results"]:
            latest_message = result["latest_message"]["content"]
            latest_message_list.append(latest_message)
        assert response.status_code == 200
        assert json_response["count"] == 2
        assert self.message2.content in latest_message_list
        assert self.message3.content in latest_message_list
