from django.urls import path

from apps.views import (
    # Product
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,

    # Cart
    CartListView, CartDetailView, CartDeleteView,

    # ProductColor
    ProductColorListView, ProductColorCreateView, ProductColorUpdateView, ProductColorDeleteView,

    # Order
    OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView,

    # Category
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, UserListView,
    UserDetailView, UserCreateView, UserUpdateView, UserDeleteView,
)

urlpatterns = [
    # Product endpoints
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Cart endpoints
    path('carts/', CartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('carts/<int:pk>/delete/', CartDeleteView.as_view(), name='cart-delete'),

    # ProductColor endpoints
    path('product-colors/', ProductColorListView.as_view(), name='productcolor-list'),
    path('product-colors/create/', ProductColorCreateView.as_view(), name='productcolor-create'),
    path('product-colors/<int:pk>/update/', ProductColorUpdateView.as_view(), name='productcolor-update'),
    path('product-colors/<int:pk>/delete/', ProductColorDeleteView.as_view(), name='productcolor-delete'),

    # Order endpoints
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),

    # Category endpoints
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),

]
