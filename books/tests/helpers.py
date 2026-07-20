from django.urls import reverse

from books.models import Book

URL = reverse("books:book-list")


def detail_url(book_id):
    return reverse("books:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "Sample title",
        "author": "Sample author",
        "cover": Book.CoverChoices.HARD,
        "inventory": 2,
        "daily_fee": "1.45",
    }
    defaults.update(params)

    return Book.objects.create(**defaults)
