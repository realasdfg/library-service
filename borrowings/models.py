from django.db import models
from django.db.models import F, Q

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(actual_return_date__gte=F("borrow_date")),
                name="expected_return_date_gte_borrow_date_borrowing",
            ),
            models.CheckConstraint(
                condition=Q(expected_return_date__gte=F("borrow_date")),
                name="actual_return_date_gte_borrow_date_borrowing",
            ),
        ]
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.book.title} - {self.user.email}"
