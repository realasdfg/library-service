from django.contrib import admin

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "inventory", "daily_fee")
    list_filter = ("author",)
    search_fields = ("title",)
