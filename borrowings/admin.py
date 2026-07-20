from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "book__title",
        "user__email",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
    )
    list_filter = ("book__title", "user__email", "borrow_date", "expected_return_date")
    search_fields = ("book__title",)
