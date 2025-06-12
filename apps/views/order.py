from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Order
from apps.serializers import OrderSerializer
from permissions import IsSuperuser


@extend_schema(tags=["Order List"])
class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["Order Create"])
class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["Order Update"])
class OrderUpdateView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["Order Delete"])
class OrderDeleteView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]
