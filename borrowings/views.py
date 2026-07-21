from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingCreateSerializer, BorrowingReadSerializer


class BorrowingViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("book")
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
