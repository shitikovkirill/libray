from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    def setUp(self):
        password = "strongpass1"
        user = get_user_model().objects.create(username="user1", email="user1@mial.com")
        user.set_password(password)
        user.save()

        url = reverse("accounts:token_create")
        data = {"username": "user1", "password": "strongpass1"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user_token = response.data["access"]

    def test_register_user(self):
        url = reverse("accounts:user-list")
        data = {
            "username": "test_user",
            "email": "test_user@mial.com",
            "password": "strongpass1",
        }

        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "test_user")

    def test_register_user_fail_email(self):
        url = reverse("accounts:user-list")
        data = {
            "username": "test_user",
            "email": "test_usermial.com",
            "password": "strongpass1",
        }

        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address.", response.data["email"])

    def test_register_user_with_authenticated_user(self):
        url = reverse("accounts:user-list")
        data = {
            "username": "test_user2",
            "email": "test_user2@mial.com",
            "password": "strongpass1",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.test_user_token)
        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "test_user2")

    def test_token(self):
        url = reverse("accounts:token_create")
        data = {"username": "user1", "password": "strongpass1"}

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["access"])

    def test_token_fail(self):
        url = reverse("accounts:token_create")
        data = {"username": "user_not_in_db", "password": "strongpass1"}

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data["detail"])
        self.assertIn(
            "No active account found with the given credentials",
            response.data["detail"],
        )

    def test_get_users_with_authenticated_user_not_admin(self):
        url = reverse("accounts:user-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.test_user_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            "You do not have permission to perform this action.",
            response.data["detail"],
        )
