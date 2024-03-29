import json

from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.factory import UserFactory
from accounts.utils import temporary_image
from apis.factory import GardenFactory, TestHelper

from .models import Comment, Conversation, Garden, Message, Photo, User


class TestCreateGarden(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "hello@world", "hello_world_123"
        )

    def test_can_create_garden_with_valid_attributes(self):

        data = GardenFactory.create_garden_dict(
            user_id=str(self.user.id), title="mylene")
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/gardens", data, format="json")
        assert response.status_code == 201
        assert Garden.objects.count() == 1
        assert Garden.objects.get().title == "mylene"

    def test_cannot_create_garden_with_zipcode_too_long(self):

        data = GardenFactory.create_garden_dict(
            user_id=str(self.user.id), zipcode="469999")

        self.client.force_authenticate(user=self.user)
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
        data = GardenFactory.create_garden_dict(
            user_id=str(self.user.id), title=random_string_more_than_hundred_char
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/gardens", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["title"] == [
            "Ensure this field has no more than 100 characters."
        ]

    def test_cannot_create_garden_if_user_does_not_exist(self):
        data = GardenFactory.create_garden_dict(user_id="4")
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/gardens", data, format="json")
        assert response.status_code == 404


class TestListGardens(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "hello@world", "hello_world_123", nickname="foo"
        )
        self.user2 = User.objects.create_user(
            "hey@world.fr", "hekolololololo", nickname="bar"
        )
        self.garden = Garden.objects.create(
            user_id=self.user.id, title="toto", zipcode="75001"
        )
        self.garden2 = Garden.objects.create(
            user_id=self.user2.id, title="tata", zipcode="93100"
        )
        self.garden3 = Garden.objects.create(
            user_id=self.user2.id, title="titi", zipcode="75001"
        )

    def test_should_list_all_gardens(self):
        response = self.client.get("/api/gardens")
        json_response = json.loads(response.content)
        res_list = [res["user_id"] for res in json_response["results"]]

        assert response.status_code == 200
        assert json_response["count"] == 3
        assert self.user.id in res_list
        assert self.user2.id in res_list

    def test_should_list_all_gardens_with_user_info(self):
        response = self.client.get("/api/gardens")
        json_response = json.loads(response.content)
        res_list = [res["user_id"] for res in json_response["results"]]
        user_list = [res["user"] for res in json_response["results"]]
        user_nicknames = [res["nickname"] for res in user_list]
        user_profile_images = [res["profile_image"] for res in user_list]

        assert response.status_code == 200
        assert json_response["count"] == 3
        assert self.user.id in res_list
        assert self.user2.id in res_list
        assert self.user.nickname in user_nicknames
        assert self.user2.nickname in user_nicknames
        assert len(user_profile_images) == 3

    def test_should_accept_filter_on_user_and_list_gardens(self):
        response = self.client.get("/api/gardens", {"user_id": self.user2.id})
        json_response = json.loads(response.content)
        user_id_list = [res["user_id"] for res in json_response["results"]]
        garden_id_list = [res["id"] for res in json_response["results"]]

        assert response.status_code == 200
        assert json_response["count"] == 2
        assert self.user.id not in user_id_list
        assert self.garden.id not in garden_id_list

    def test_should_accept_filter_on_zipcode_and_list_gardens(self):
        response = self.client.get("/api/gardens", {"zipcode": "75001"})
        json_response = json.loads(response.content)
        zipcode_list = [res["zipcode"] for res in json_response["results"]]

        assert response.status_code == 200
        assert json_response["count"] == 2
        assert "93100" not in zipcode_list


class TestUdateGarden(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "hello@world", "hello_world_123"
        )
        self.user2 = User.objects.create_user(
            "hey@world.fr", "hekolololololo"
        )
        self.garden = Garden.objects.create(
            user_id=self.user.id, title="toto", zipcode="75001"
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
            "hello@world", "hello_world_123"
        )
        for i in range(12):
            self.garden = Garden.objects.create(user_id=self.user.id)

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
        data = {"author_id": user.id,
                "receiver_id": user2.id, "content": "coucou"}
        response = self.client.post("/api/comments", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 201
        assert json_response["author_id"] == user.id
        assert json_response["receiver_id"] == user2.id
        assert json_response["content"] == data["content"]

    def test_with_unauthenticated_user_should_fail(self):
        user = UserFactory.create_user()
        user2 = UserFactory.create_user()
        data = {"author_id": user.id,
                "receiver_id": user2.id, "content": "Hello"}

        response = self.client.post("/api/comments", data, format="json")
        assert response.status_code == 401


class TestFetchCommentsOfAGivenUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hello@world", "hello_world_123")
        self.user2 = User.objects.create_user("foo@bar.lol", "foobarlol")
        self.comment = Comment.objects.create(
            receiver_id=self.user.id, author_id=self.user2.id
        )
        self.comment2 = Comment.objects.create(
            receiver_id=self.user2.id, author_id=self.user.id
        )

    def test_should_fetch_author_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/comments?receiver_id={self.user.id}")
        json_response = json.loads(response.content)
        receiver_id_list = [res["id"] for res in json_response["results"]]
        author_list = [res["author"] for res in json_response["results"]]
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
            user_id=self.user.id, title="toto", zipcode="75001"
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
            user_id=self.user.id, title="toto", zipcode="75001"
        )

        self.user2 = User.objects.create_user(
            "hola@world.fr", "hekolololololo")

        self.garden2 = Garden.objects.create(
            user_id=self.user2.id, title="toto", zipcode="75001"
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

        garden_id_list = [item["garden_id"]
                          for item in json_response["results"]]
        assert self.garden.id in garden_id_list
        assert self.garden2.id in garden_id_list

    def test_should_accept_garden_id_as_params_and_list_all_photos(self):
        response = self.client.get(f"/api/photos?garden_id={self.garden.id}")
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response["count"] == 1

        garden_id_list = [item["garden_id"]
                          for item in json_response["results"]]

        assert self.garden.id in garden_id_list
        assert self.garden2.id not in garden_id_list


class TestUpdatePhotos(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.garden = Garden.objects.create(
            user_id=self.user.id, title="toto", zipcode="75001"
        )

        self.user2 = User.objects.create_user(
            "hola@world.fr", "hekolololololo")

        self.garden2 = Garden.objects.create(
            user_id=self.user2.id, title="toto", zipcode="75001"
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
        data = {"garden_id": self.garden.id,
                "season": 3, "is_main_photo": True}
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

        data = {"garden_id": self.garden2.id,
                "season": 3, "is_main_photo": True}
        response = self.client.put(f"/api/photos/{photo.id}", data=data)
        assert response.status_code == 403


class TestListConversationsWithLatestMessage(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.user2 = User.objects.create_user(
            "hola@world.fr", "hekolololololo")
        self.conversation = Conversation.objects.create(
            chat_sender_id=self.user.id, chat_receiver_id=self.user2.id
        )
        self.message = Message.objects.create(
            sender_id=self.user.id,
            content="Hello there",
            conversation_id=self.conversation.id,
            sent_at=timezone.now() - timezone.timedelta(hours=1),
        )
        self.message2 = Message.objects.create(
            sender_id=self.user.id,
            content="Latest msg",
            conversation_id=self.conversation.id,
            sent_at=timezone.now(),
        )

    def test_should_return_401_if_not_authenticated(self):
        response = self.client.get("/api/conversations")
        assert response.status_code == 401

    def test_should_return_403_if_not_part_of_the_conversation(self):
        self.user3 = User.objects.create_user(
            "test@test.test", "testingtesting")
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(
            f"/api/conversations?current_user_id={self.user3.id}")
        assert response.status_code == 403

    def test_should_return_403_if_the_query_param_is_not_provided(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            "/api/conversations")
        assert response.status_code == 403

    def test_should_return_the_latest_message_of_conversation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f"/api/conversations?current_user_id={self.user.id}")
        json_response = json.loads(response.content)
        assert response.status_code == 200
        latest_message_list = [item["latest_message"]["content"]
                               for item in json_response["results"]]
        assert self.message2.content in latest_message_list
        assert self.message.content not in latest_message_list

    def test_should_list_all_conversations_with_latest_message_for_the_given_user(self):
        self.conversation2 = Conversation.objects.create(
            chat_sender_id=self.user2.id, chat_receiver_id=self.user.id
        )
        self.message3 = Message.objects.create(
            sender_id=self.user2.id,
            content="Another msg",
            conversation_id=self.conversation2.id,
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f"/api/conversations?current_user_id={self.user.id}")
        json_response = json.loads(response.content)
        latest_message_list = [item["latest_message"]["content"]
                               for item in json_response["results"]]
        assert response.status_code == 200
        assert json_response["count"] == 2
        assert self.message2.content in latest_message_list
        assert self.message3.content in latest_message_list

    def test_should_return_empty_object_if_no_latest_message(self):
        self.conversation2 = Conversation.objects.create(
            chat_sender_id=self.user2.id, chat_receiver_id=self.user.id)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(
            f"/api/conversations?current_user_id={self.user2.id}")
        json_response = json.loads(response.content)
        latest_messages = [
            item["latest_message"] for item in json_response["results"]]
        assert {} in latest_messages


class TestShowConversationWithAllMessages(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.user2 = User.objects.create_user(
            "hola@world.fr", "hekolololololo")
        self.conversation = Conversation.objects.create(
            chat_sender_id=self.user.id, chat_receiver_id=self.user2.id
        )
        self.message = Message.objects.create(
            sender_id=self.user.id,
            content="Hello there",
            conversation_id=self.conversation.id,
            sent_at=timezone.now() - timezone.timedelta(hours=1),
        )
        self.message2 = Message.objects.create(
            sender_id=self.user.id,
            content="Latest msg",
            conversation_id=self.conversation.id,
            sent_at=timezone.now(),
        )

    def test_should_return_401_if_not_authenticated(self):
        response = self.client.get(
            f"/api/conversations/{self.conversation.id}")
        assert response.status_code == 401

    def test_should_return_403_if_not_part_of_the_conversation(self):
        self.user3 = User.objects.create_user(
            "test@test.test", "testingtesting")
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(
            f"/api/conversations/{self.conversation.id}")
        assert response.status_code == 403

    def test_should_return_all_messages_for_the_given_conversation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f"/api/conversations/{self.conversation.id}?current_user_id={self.user.id}")
        json_response = json.loads(response.content)
        print(json_response)
        member_ids = [
            json_response["chat_sender_id"],
            json_response["chat_receiver_id"],
        ]
        assert response.status_code == 200
        assert any(
            message["content"] == self.message.content
            for message in json_response["messages"]
        )
        assert any(
            message["content"] == self.message2.content
            for message in json_response["messages"]
        )
        assert json_response["id"] == self.conversation.id
        assert self.user.id in member_ids
        assert self.user2.id in member_ids

    def test_should_return_empty_list_if_no_messages_for_the_given_conversation(self):
        self.user3 = User.objects.create_user(
            "testing@test.test", "testingfoobar")
        self.conversation2 = Conversation.objects.create(
            chat_sender_id=self.user3.id, chat_receiver_id=self.user.id)
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(
            f"/api/conversations/{self.conversation2.id}?current_user_id={self.user3.id}")
        json_response = json.loads(response.content)
        assert json_response["messages"] == []


class TestCreateConversation(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.user2 = User.objects.create_user(
            "hola@world.fr", "hekolololololo")

    def test_should_return_401_if_not_authenticated(self):
        data = {"chat_sender_id": self.user.id,
                "chat_receiver_id": self.user2.id}
        response = self.client.post(
            "/api/conversations", data=data, format="json")
        assert response.status_code == 401

    def test_should_create_a_conversation_if_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"chat_sender_id": self.user.id,
                "chat_receiver_id": self.user2.id}
        response = self.client.post(
            "/api/conversations", data=data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 201
        assert json_response["chat_sender_id"] == self.user.id
        assert json_response["chat_receiver_id"] == data["chat_receiver_id"]

    def test_should_return_400_and_conversation_id_if_conversation_between_two_users_already_exists(self):
        self.conversation = Conversation.objects.create(
            chat_sender_id=self.user.id, chat_receiver_id=self.user2.id)
        self.client.force_authenticate(user=self.user)
        data = {"chat_sender_id": self.user.id,
                "chat_receiver_id": self.user2.id}
        response = self.client.post(
            "/api/conversations", data=data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["error"] == "Conversation already exists between these two users"
        assert json_response["conversation_id"] == str(self.conversation.id)


class TestCreatePrivateMessages(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hey@world.fr", "hekolololololo")
        self.user2 = User.objects.create_user(
            "hola@world.fr", "hekolololololo")
        self.conversation = Conversation.objects.create(
            chat_sender_id=self.user.id, chat_receiver_id=self.user2.id
        )

    def test_should_return_401_if_not_authenticated(self):
        response = self.client.post("/api/messages")
        assert response.status_code == 401

    def test_should_return_403_if_not_part_of_conversation(self):
        self.user3 = User.objects.create_user("hola@hola.es", "holaholahola")
        self.client.force_authenticate(user=self.user3)
        data = {
            "conversation_id": self.conversation.id,
            "content": "I can't send anything.",
        }
        response = self.client.post("/api/messages", data=data, format="json")
        assert response.status_code == 403

    def test_can_post_messages_if_conversation_owner_or_receiver(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "conversation_id": self.conversation.id,
            "content": "Hello World",
        }
        response = self.client.post("/api/messages", data=data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 201
        assert json_response["conversation_id"] == data["conversation_id"]
        assert json_response["content"] == data["content"]
        assert json_response["sender_id"] == self.user.id
        assert json_response["sent_at"] is not None
