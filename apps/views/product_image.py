from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from apps.models import ProductImage
from apps.serializers import ProductImageSerializer


@extend_schema(tags=["ProductImage List"])
class ProductImageListView(ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


@extend_schema(tags=["ProductImage Detail"])
class ProductImageDetailView(RetrieveAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


@extend_schema(tags=["ProductImage Create"])
class ProductImageCreateView(CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


@extend_schema(tags=["ProductImage Update"])
class ProductImageUpdateView(UpdateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


@extend_schema(tags=["ProductImage Delete"])
class ProductImageDeleteView(DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
