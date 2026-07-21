from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from books.models import Book
from books.serializers import BookSerializer
from users.permissions import IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of Books",
        description="Returns a list of all books. Available to all users (read-only).",
        tags=["Books"],
    ),
    retrieve=extend_schema(
        summary="Retrieve the book",
        description="Returns only one book by ID. Available to all users (read-only).",
        tags=["Books"],
    ),
    create=extend_schema(
        summary="Create a new book",
        description="Creates a book. Available only to administrators.",
        tags=["Books"],
    ),
    update=extend_schema(
        summary="Refresh the entire book",
        description="Updates entire book by ID. Available only to administrators.",
        tags=["Books"],
    ),
    partial_update=extend_schema(
        summary="Partially update the book",
        description="Partially updates book by ID. Available only to administrators.",
        tags=["Books"],
    ),
    destroy=extend_schema(
        summary="Delete the book",
        description="Deletes a book by ID. Available only to administrators.",
        tags=["Books"],
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
