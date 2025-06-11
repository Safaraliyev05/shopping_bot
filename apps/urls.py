from django.urls import path

from apps.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    # Product endpoints
    path('Products/', ProductListView.as_view(), name='Product-list'),
    path('Products/<int:pk>/', ProductDetailView.as_view(), name='Product-detail'),
    path('Products/create/', ProductCreateView.as_view(), name='Product-create'),
    path('Products/<int:pk>/update/', ProductUpdateView.as_view(), name='Product-update'),
    path('Products/<int:pk>/delete/', ProductDeleteView.as_view(), name='Product-delete'),
]
