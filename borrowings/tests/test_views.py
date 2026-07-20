from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

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
