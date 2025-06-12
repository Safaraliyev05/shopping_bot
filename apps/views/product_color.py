from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import ProductColor
from apps.serializers import ProductColorSerializer
from permissions import IsSuperuser


@extend_schema(tags=["ProductColor List"])
class ProductColorListView(ListAPIView):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["ProductColor Create"])
class ProductColorCreateView(CreateAPIView):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["ProductColor Update"])
class ProductColorUpdateView(UpdateAPIView):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]


@extend_schema(tags=["ProductColor Delete"])
class ProductColorDeleteView(DestroyAPIView):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]
