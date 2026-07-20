from django.urls import include, path
from rest_framework import routers

from borrowings.views import BorrowingReadViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingReadViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowings"
