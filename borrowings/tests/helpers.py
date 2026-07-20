from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse

from books.tests.helpers import sample_book
from borrowings.models import Borrowing

User = get_user_model()

URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


def sample_borrowing(**params):
    user_count = User.objects.count()
    user = params.get(
        "user",
        User.objects.create_user(
            email=f"user{user_count}@example.com", password="qwerqwer"
        ),
    )
    defaults = {
        "expected_return_date": params.get(
            "expected_return_date", date.today() + timedelta(days=1)
        ),
        "actual_return_date": params.get(
            "actual_return_date", date.today() + timedelta(days=1)
        ),
        "book": params.get("book", sample_book()),
        "user": user,
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)
