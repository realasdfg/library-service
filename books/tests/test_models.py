from django.test import TestCase

from books.models import Book
from books.tests.helpers import sample_book


class TestBook(TestCase):
    def setUp(self):
        self.book = sample_book()

    def test_str_representation(self):
        self.assertEqual(str(self.book), "Sample title")

    def test_inventory_default_value(self):
        self.assertEqual(self.book.inventory, 2)

    def test_ordering_by_title(self):
        sample_book(title="The Three-Body Problem")
        titles = list(Book.objects.values_list("title", flat=True))
        self.assertEqual(titles, sorted(titles))
