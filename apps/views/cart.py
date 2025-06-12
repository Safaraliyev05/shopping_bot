from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Cart
from apps.serializers import CartSerializer
from permissions import IsSuperuser


@extend_schema(tags=["Cart List"])
class CartListView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["Cart Detail"])
class CartDetailView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["Cart Delete"])
class CartDeleteView(DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]
