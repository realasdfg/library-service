from datetime import date

from django.db import transaction
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from borrowings.filters import BorrowingFilter
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingReadSerializer,
    EmptySerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of current user borrowings",
        description="Returns a list of all current user borrowings. Available to authenticated users."
        "Only admins can retrieve other user borrowings.",
        tags=["Borrowings"],
        parameters=[
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by borrowing is still active (ex. ?is_active=true)",
            ),
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description="Filter by user id (ex. ?user_id=1). Available only to admins.",
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve the borrowing",
        description="Retrieve the borrowing by ID. Available to authenticated users."
        "Only admins can retrieve other user borrowings.",
        tags=["Borrowings"],
    ),
    create=extend_schema(
        summary="Create a new borrowing",
        description="Creates a borrowing for current user. Available to authenticated users",
        tags=["Borrowings"],
    ),
)
class BorrowingViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)
    filterset_class = BorrowingFilter

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("book")

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "return_borrowing":
            return EmptySerializer
        return BorrowingReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        if not borrowing.is_active:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            borrowing.actual_return_date = timezone.now().date()
            borrowing.save(update_fields=["actual_return_date"])

            book = borrowing.book
            book.inventory += 1
            book.save(update_fields=["inventory"])

        serializer = BorrowingReadSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)
