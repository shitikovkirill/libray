from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book, Loan


class BookModelTestCase(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890123",
            "page_count": 100,
            "published_date": "2025-02-16",
        }
        self.book = Book.objects.create(**self.book_data)

    def test_book_creation(self):
        self.assertEqual(self.book.title, self.book_data["title"])
        self.assertEqual(self.book.author, self.book_data["author"])
        self.assertEqual(self.book.isbn, self.book_data["isbn"])
        self.assertEqual(self.book.page_count, self.book_data["page_count"])
        self.assertEqual(
            str(self.book.published_date), self.book_data["published_date"]
        )

    def test_unique_isbn(self):
        with self.assertRaises(IntegrityError):
            Book.objects.create(**self.book_data)

    def test_booked_manager_annotation(self):
        user = get_user_model().objects.create(
            username="testuser", email="test@example.com"
        )
        Loan.objects.create(user=user, book=self.book)
        book_with_annotation = Book.booked_objects.get(id=self.book.id)
        self.assertEqual(book_with_annotation.need_return, 1)

    def test_book_str_method(self):
        self.assertEqual(str(self.book), "Test Book by Test Author")


class LoanModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=100,
            published_date="2025-02-16",
        )
        self.loan_data = {
            "user": self.user,
            "book": self.book,
        }
        self.loan = Loan.objects.create(**self.loan_data)

    def test_loan_creation(self):
        self.assertEqual(self.loan.user, self.user)
        self.assertEqual(self.loan.book, self.book)
        self.assertIsNone(self.loan.return_date)
        self.assertIsNotNone(self.loan.borrowed_date)

    def test_unique_loan_constraint(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="123456Q90123",
            page_count=100,
            published_date="2025-02-16",
        )

        Loan.objects.create(user=self.user, book=book)
        with self.assertRaises(IntegrityError):
            Loan.objects.create(user=self.user, book=book)

    def test_who_loan_method(self):
        loans = Loan.objects.who_loan(self.book)
        self.assertEqual(loans.count(), 1)
        self.assertEqual(loans.first().user, self.user)
        self.assertIsNone(loans.first().return_date)

    def test_loan_str_method(self):
        self.assertEqual(
            str(self.loan), "Test Book by Test Author borrowed by testuser"
        )


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

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.test_admin_user_token
        )
        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["id"])


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=100,
            published_date="2025-02-16",
        )
        self.url = reverse("books:book-list")

    def test_get_book_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_detail(self):
        user = get_user_model().objects.create(
            username="testuser", email="test@example.com", is_staff=True
        )
        self.client.force_authenticate(user=user)
        detail_url = reverse("books:book-detail", args=[self.book.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        user = get_user_model().objects.create(
            username="testuser", email="test@example.com", is_staff=True
        )
        self.client.force_authenticate(user=user)
        detail_url = reverse("books:book-detail", args=[self.book.id])
        updated_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "isbn": "1234567890123",
            "page_count": 200,
            "published_date": "2023-01-01",
        }
        response = self.client.put(detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        user = get_user_model().objects.create(
            username="testuser", email="test@example.com", is_staff=True
        )
        self.client.force_authenticate(user=user)
        detail_url = reverse("books:book-detail", args=[self.book.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
