from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer
from books.tests.helpers import URL, detail_url, sample_book

User = get_user_model()


class UnauthenticatedBooksTest(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()

    def test_book_list(self):
        sample_book()
        sample_book(title="Sample title2")
        serializer = BookSerializer(Book.objects.all(), many=True)

        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_book_detail(self):
        book = sample_book()
        serializer = BookSerializer(book)

        res = self.client.get(detail_url(book.pk))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_book_create_unauthorized_error(self):
        data = {
            "title": "Sample title",
            "author": "Sample author",
            "cover": Book.CoverChoices.HARD,
            "inventory": "2",
            "daily_fee": "1.45",
        }

        res = self.client.post(URL, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(Book.objects.all()), 0)

    def test_book_update_unauthorized_error(self):
        book = sample_book()
        book_title = book.title
        data = {"title": "Changed title"}

        res = self.client.patch(detail_url(book.pk), data)
        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(book_title, book.title)

    def test_book_delete_unauthorized_error(self):
        book = sample_book()
        res = self.client.delete(detail_url(book.pk))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.filter(id=book.id).count(), 1)


class AuthenticatedBooksTest(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.user = User.objects.create_user("user@example.com", "password")
        self.client.force_authenticate(self.user)

    def test_book_create_forbidden_error(self):
        data = {
            "title": "Sample title",
            "author": "Sample author",
            "cover": Book.CoverChoices.HARD,
            "inventory": "2",
            "daily_fee": "1.45",
        }

        res = self.client.post(URL, data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(Book.objects.all()), 0)

    def test_book_update_forbidden_error(self):
        book = sample_book()
        book_title = book.title
        data = {"title": "Changed title"}

        res = self.client.patch(detail_url(book.pk), data)
        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(book_title, book.title)

    def test_book_delete_forbidden_error(self):
        book = sample_book()
        res = self.client.delete(detail_url(book.pk))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.filter(id=book.id).count(), 1)


class AdminBooksTest(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.user = User.objects.create_superuser("user@example.com", "password")
        self.client.force_authenticate(self.user)

    def test_book_create(self):
        data = {
            "title": "Sample title",
            "author": "Sample author",
            "cover": Book.CoverChoices.HARD,
            "inventory": "2",
            "daily_fee": "1.45",
        }

        res = self.client.post(URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Book.objects.all()), 1)

    def test_book_update(self):
        book = sample_book()
        data = {"title": "Changed title"}

        res = self.client.patch(detail_url(book.pk), data)
        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], book.title)

    def test_book_delete(self):
        book = sample_book()
        res = self.client.delete(detail_url(book.pk))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.filter(id=book.id).count(), 0)
