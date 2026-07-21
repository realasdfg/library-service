from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from books.tests.helpers import sample_book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingReadSerializer
from borrowings.tests.helpers import URL, detail_url, sample_borrowing

User = get_user_model()


class UnauthenticatedBorrowingTest(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()

    def test_unauthorized_error(self):
        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingTest(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.user = User.objects.create_user("user@example.com", "password")
        self.client.force_authenticate(self.user)

    def test_borrowing_list(self):
        sample_borrowing(user=self.user)
        sample_borrowing(user=self.user)
        serializer = BorrowingReadSerializer(Borrowing.objects.all(), many=True)

        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_list_filter_by_is_active(self):
        borrowing1 = sample_borrowing(user=self.user)
        borrowing2 = sample_borrowing(user=self.user)
        borrowing3 = sample_borrowing(user=self.user, actual_return_date=None)
        serializer1 = BorrowingReadSerializer(borrowing1)
        serializer2 = BorrowingReadSerializer(borrowing2)
        serializer3 = BorrowingReadSerializer(borrowing3)

        res = self.client.get(URL, {"is_active": "true"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)

    def test_borrowing_list_not_admin_filter_by_user_id(self):
        another_user = User.objects.create_user(
            email="some@example.com", password="qwertyqwer"
        )
        borrowing1 = sample_borrowing(user=another_user)
        borrowing2 = sample_borrowing(user=another_user)
        borrowing3 = sample_borrowing(user=self.user)
        serializer1 = BorrowingReadSerializer(borrowing1)
        serializer2 = BorrowingReadSerializer(borrowing2)
        serializer3 = BorrowingReadSerializer(borrowing3)

        res = self.client.get(URL, {"user_id": f"{another_user.id}"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_borrowing_detail(self):
        borrowing = sample_borrowing(user=self.user)
        serializer = BorrowingReadSerializer(borrowing)

        res = self.client.get(detail_url(borrowing.pk))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_retrieve_only_their_borrowings(self):
        borrowing1 = sample_borrowing(user=self.user)
        borrowing2 = sample_borrowing(user=self.user)
        borrowing3 = sample_borrowing()
        serializer1 = BorrowingReadSerializer(borrowing1)
        serializer2 = BorrowingReadSerializer(borrowing2)
        serializer3 = BorrowingReadSerializer(borrowing3)

        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_borrowing_create(self):
        book = sample_book(inventory=1)
        data = {
            "expected_return_date": date.today() + timedelta(days=1),
            "book": book.pk,
        }
        res = self.client.post(URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        borrowing = Borrowing.objects.get(pk=res.data["id"])
        self.assertEqual(borrowing.expected_return_date, data["expected_return_date"])
        self.assertIsNone(borrowing.actual_return_date)
        self.assertEqual(borrowing.borrow_date, date.today())
        self.assertEqual(borrowing.book, book)
        self.assertEqual(borrowing.user, self.user)


class AdminBorrowingTest(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.user = User.objects.create_superuser("admin@example.com", "password")
        self.client.force_authenticate(self.user)

    def test_admin_retrieve_all_borrowings(self):
        borrowing1 = sample_borrowing(user=self.user)
        borrowing2 = sample_borrowing()
        serializer1 = BorrowingReadSerializer(borrowing1)
        serializer2 = BorrowingReadSerializer(borrowing2)

        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_borrowing_list_filter_by_user_id(self):
        another_user = User.objects.create_user(
            email="user@example.com", password="qwertyqwer"
        )
        borrowing1 = sample_borrowing(user=another_user)
        borrowing2 = sample_borrowing(user=another_user)
        borrowing3 = sample_borrowing(user=self.user)
        serializer1 = BorrowingReadSerializer(borrowing1)
        serializer2 = BorrowingReadSerializer(borrowing2)
        serializer3 = BorrowingReadSerializer(borrowing3)

        res = self.client.get(URL, {"user_id": f"{another_user.id}"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
