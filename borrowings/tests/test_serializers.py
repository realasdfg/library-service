from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from books.tests.helpers import sample_book
from borrowings.serializers import BorrowingCreateSerializer

User = get_user_model()


class BorrowingCreateSerializerTest(TestCase):
    def test_create_borrowing_success(self):
        book = sample_book(inventory=1)
        data = {
            "expected_return_date": date.today() + timedelta(days=1),
            "book": book.pk,
        }
        serializer = BorrowingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create_borrowing_book_ot_of_stock(self):
        book = sample_book(inventory=0)
        data = {
            "expected_return_date": date.today() + timedelta(days=1),
            "book": book.pk,
        }
        serializer = BorrowingCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_borrowing_expected_return_date_bedore_today(self):
        book = sample_book(inventory=0)
        data = {
            "expected_return_date": date.today() - timedelta(days=1),
            "book": book.pk,
        }
        serializer = BorrowingCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_borrowing_decreases_book_inventory(self):
        book = sample_book(inventory=1)
        data = {
            "expected_return_date": date.today() + timedelta(days=1),
            "book": book.pk,
        }
        serializer = BorrowingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save(
            user=User.objects.create_user(
                email="user@example.com", password="qwertyqwe"
            )
        )
        book.refresh_from_db()
        self.assertEqual(book.inventory, 0)
