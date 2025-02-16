from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BookTestCase(APITestCase):

    def test_create_book(self):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "test_user2")
