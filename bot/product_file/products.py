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
