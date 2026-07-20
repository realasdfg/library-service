from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingReadSerializer


class BorrowingReadViewSet(ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related("book")
