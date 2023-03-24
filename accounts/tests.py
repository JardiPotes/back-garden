import json

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .factory import UserFactory
from .models import User
from .utils import temporary_image


class TestRegisterUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("john@snow.com", "johnpassword")
        self.client.login(email="john@snow.com", password="johnpassword")

    def test_can_create_account(self):
        data = UserFactory.create_user_dict(email="hellothere@test.test")
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        assert response.status_code == 201
        assert User.objects.count() == 2
        assert User.objects.get(email="hellothere@test.test")

    def test_should_accept_experience_from_one_to_five_on_creation(self):
        data = UserFactory.create_user_dict(experience=5)
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        json_response = json.loads(response.content)
        assert response.status_code == 201
        assert json_response["experience"] == 5

    def test_cannot_create_account_with_experience_greater_than_five(self):
        data = UserFactory.create_user_dict(experience=10)
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["experience"] == [
            "Ensure this value is less than or equal to 5."
        ]

    def test_cannot_create_account_with_experience_less_than_one(self):
        data = UserFactory.create_user_dict(experience=0)
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["experience"] == [
            "Ensure this value is greater than or equal to 1."
        ]

    def test_cannot_create_account_with_experience_set_as_decimal(self):
        data = UserFactory.create_user_dict(experience=1.3)
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["experience"] == ["A valid integer is required."]

    def test_cannot_create_account_with_invalid_email(self):
        data = UserFactory.create_user_dict(email="lol.l")
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["email"] == ["Enter a valid email address."]

    def test_cannot_create_user_with_already_existed_email(self):
        data = UserFactory.create_user_dict(email="john@snow.com")
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        json_response = json.loads(response.content)

        assert response.status_code == 400
        assert json_response["email"] == [
            "user with this email address already exists."
        ]

    def test_cannot_create_user_with_password_less_than_8_chars(self):
        data = UserFactory.create_user_dict(password="123")
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response["password"] == [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common.",
            "This password is entirely numeric.",
        ]

    def test_should_accept_uploaded_images_on_creation(self):
        data = UserFactory.create_user_dict(profile_image=temporary_image())
        response = self.client.post(
            "/api/auth/register", data, format="multipart")
        assert response.status_code == 201


class TestUserLogin(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("john@snow.com", "johnpassword")
        self.token = Token.objects.create(user=self.user)

    def test_can_login_with_valid_email_password(self):
        data = {"email": "john@snow.com", "password": "johnpassword"}
        response = self.client.post(
            "/api/auth/login",
            data,
            format="json",
            HTTP_AUTHORIZATION="Token {}".format(self.token),
        )
        assert response.status_code == 200

    def test_when_successfully_logged_in_returns_user_info(self):
        data = {"email": "john@snow.com", "password": "johnpassword"}
        response = self.client.post(
            "/api/auth/login",
            data,
            format="json",
            HTTP_AUTHORIZATION="Token {}".format(self.token),
        )
        json_response = json.loads(response.content)
        assert json_response["user"]["id"] == self.user.id

    def test_cannot_login_with_invalid_email_or_password(self):
        data = {"email": "john@snow.com", "password": "123"}
        response = self.client.post("/api/auth/login", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 400
        assert json_response == ["Invalid email/password. Please try again!"]


class TestUserLogout(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("john@snow.com", "johnpassword")

    def test_can_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/auth/logout")
        assert response.status_code == 200


class TestListUsers(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("john@snow.com", "johnpassword")
        self.user = User.objects.create_user("hello@lol.fr", "hellofoobar")

    def test_can_list_all_users(self):

        response = self.client.get("/api/users")
        assert response.status_code == 200
        assert User.objects.count() == 2


class TestGetUserDetail(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("john@snow.com", "johnpassword")
        self.user2 = User.objects.create_user("hello@lol.fr", "hellofoobar")

    def test_can_get_user_info_by_id(self):
        response = self.client.get(f"/api/users/{self.user.id}")
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response["id"] == self.user.id


class TestResetPassword(APITestCase):
    def setUp(self):
        user = User.objects.create_user("hello@world", "hello_world_123")
        self.client.force_authenticate(user=user)

    def test_can_reset_password_with_correct_credentials(self):
        data = {
            "current_password": "hello_world_123",
            "new_password": "new_hello_world_123",
        }
        response = self.client.post(
            "/api/auth/password_change", data=data, format="json"
        )
        assert response.status_code == 204


class TestUpdateUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "hello@foo.bar", "foobar12345", bio="foobar"
        )

    def test_can_edit_user_profile_with_correct_user_id(self):
        self.client.force_authenticate(user=self.user)

        data = {"bio": "barfoo"}
        response = self.client.put(
            f"/api/users/{self.user.id}", data, format="json")
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response["bio"] == "barfoo"

    def test_can_upload_a_new_profile_photo_with_correct_id(self):
        self.client.force_authenticate(user=self.user)

        data = {"profile_image": temporary_image()}
        response = self.client.put(
            f"/api/users/{self.user.id}", data, format="multipart"
        )
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response["profile_image"] is not None
