from datetime import date

from django.db import transaction
from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "expected_return_date",
            "book",
        )

    def validate_book(self, value):
        if value.inventory < 1:
            raise serializers.ValidationError(
                "This book is out of stock. Please try again later."
            )
        return value

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        if attrs["expected_return_date"] < date.today():
            raise serializers.ValidationError(
                "expected_return_date can't be before today's date."
            )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            book = Book.objects.select_for_update().get(pk=validated_data["book"].pk)
            book.inventory -= 1
            book.save()
            return super().create(validated_data)
