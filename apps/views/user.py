from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from apps.models import User
from apps.serializers import UserSerializer


@extend_schema(tags=["User List"])
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["User Detail"])
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["User Create"])
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["User Update"])
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["User Delete"])
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
