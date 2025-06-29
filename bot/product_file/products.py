from asgiref.sync import sync_to_async

from apps.models import ProductColor


def get_all_product_data():
    products = ProductColor.objects.select_related('product').all()
    return [
        {
            'id': pc.id,
            'name': pc.product.name_uz,
            'price': pc.price,
        } for pc in products
    ]


@sync_to_async
def get_products_by_category_id(category_id):
    product_colors = ProductColor.objects.filter(
        product__categories__id=category_id
    ).select_related('product').distinct()

    return [
        {
            'id': pc.id,
            'name': pc.product.name_uz,
            'price': pc.price,
        } for pc in product_colors
    ]
