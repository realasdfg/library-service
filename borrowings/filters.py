import django_filters

from borrowings.models import Borrowing


class BorrowingFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        field_name="actual_return_date", lookup_expr="isnull"
    )
    user_id = django_filters.NumberFilter(field_name="user", lookup_expr="id")

    class Meta:
        model = Borrowing
        fields = ("is_active", "user_id")
