from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Register a new user",
        description="Register a new user in the system. Available to all users",
    ),
)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve currently logged in user",
        description="Retrieves currently logged in user. Available to authenticated users",
    ),
    put=extend_schema(
        summary="Fully update currently logged in user",
        description="Updates currently logged in user. Available to authenticated users",
    ),
    patch=extend_schema(
        summary="Partially update currently logged in user",
        description="Partially updates currently logged in user. Available to authenticated users",
    ),
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
