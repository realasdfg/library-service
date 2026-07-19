from decimal import Decimal
from unittest import TestCase

from books.models import Book


class TestBook(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="1984",
            author="George Orwell",
            cover=Book.CoverChoices.HARD,
            daily_fee=Decimal("2.50"),
        )

    def test_str_representation(self):
        self.assertEqual(str(self.book), "1984")

    def test_inventory_default_value(self):
        self.assertEqual(self.book.inventory, 0)

    def test_ordering_by_title(self):
        Book.objects.create(
            title="The Three-Body Problem",
            author="Liu Cixin",
            cover=Book.CoverChoices.HARD,
            daily_fee=Decimal("3.00"),
        )
        titles = list(Book.objects.values_list("title", flat=True))
        self.assertEqual(titles, sorted(titles))
