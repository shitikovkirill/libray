from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BookTestCase(APITestCase):
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
        
        user = get_user_model().objects.create_superuser(
            username="user2", email="user2@mial.com"
        )
        user.set_password(password)
        user.save()

        data = {"username": user.username, "password": password}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_admin_user_token = response.data["access"]

    def test_create_book_without_autentification(self):
        url = reverse("books:book-list")
        data = {
            "title": "Book titlr",
            "author": "Author",
            "isbn": "dfgdfgfdvc",
            "page_count": 56,
            "published_date": "2025-02-16",
        }

        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            "Authentication credentials were not provided.",
            response.data["detail"],
        )

    def test_create_book_without_autentification(self):
        url = reverse("books:book-list")
        data = {
            "title": "Book titlr",
            "author": "Author",
            "isbn": "dfgdfgfdvc",
            "page_count": 56,
            "published_date": "2025-02-16",
        }

        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            "Authentication credentials were not provided.",
            response.data["detail"],
        )

    def test_create_book_without_autentification(self):
        url = reverse("books:book-list")
        data = {
            "title": "Book titlr",
            "author": "Author",
            "isbn": "dfgdfgfdvc",
            "page_count": 56,
            "published_date": "2025-02-16",
        }

        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            "Authentication credentials were not provided.",
            response.data["detail"],
        )

    def test_create_book_with_autentification_not_admin(self):
        url = reverse("books:book-list")
        data = {
            "title": "Book titlr",
            "author": "Author",
            "isbn": "dfgdfgfdvc",
            "page_count": 56,
            "published_date": "2025-02-16",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.test_user_token)
        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            "You do not have permission to perform this action.",
            response.data["detail"],
        )

    def test_create_book_with_autentification_admin(self):
        url = reverse("books:book-list")
        data = {
            "title": "Book titlr",
            "author": "Author",
            "isbn": "dfgdfgfdvc",
            "page_count": 56,
            "published_date": "2025-02-16",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.test_admin_user_token)
        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["id"])
