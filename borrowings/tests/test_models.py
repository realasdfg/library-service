from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from books.tests.helpers import sample_book
from borrowings.models import Borrowing

User = get_user_model()


class TestBorrowing(TestCase):
    def setUp(self):
        self.book = sample_book()
        self.user = User.objects.create_user(
            email="user@example.com", password="qwerqwer"
        )
        self.borrowing = Borrowing.objects.create(
            expected_return_date=date.today() + timedelta(days=1),
            actual_return_date=date.today() + timedelta(days=1),
            book=self.book,
            user=self.user,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.borrowing), f"{self.book.title} - {self.user.email}")


class TestBorrowingCreate(TestCase):
    def setUp(self):
        self.book = sample_book()
        self.user = User.objects.create_user(
            email="user@example.com", password="qwerqwer"
        )

    def test_expected_return_date_gte_borrow_date_constraint(self):
        with self.assertRaises(IntegrityError):
            self.borrowing = Borrowing.objects.create(
                expected_return_date=date.today() - timedelta(days=1),
                book=self.book,
                user=self.user,
            )

    def test_actual_return_date_gte_borrow_date_constraint(self):
        with self.assertRaises(IntegrityError):
            self.borrowing = Borrowing.objects.create(
                expected_return_date=date.today() + timedelta(days=1),
                actual_return_date=date.today() - timedelta(days=1),
                book=self.book,
                user=self.user,
            )

    def test_passes_constraints(self):
        try:
            Borrowing.objects.create(
                expected_return_date=date.today(),
                actual_return_date=date.today(),
                book=self.book,
                user=self.user,
            )
            Borrowing.objects.create(
                expected_return_date=date.today() + timedelta(days=1),
                actual_return_date=date.today() + timedelta(days=1),
                book=self.book,
                user=self.user,
            )
        except IntegrityError:
            self.fail("test_passes_constraints() raised IntegrityError unexpectedly!")
