from asgiref.sync import sync_to_async

from apps.models import ProductColor


@sync_to_async
def get_products_by_category(category_id):
    return [
        {
            'id': pc.id,
            'name': pc.product.name_uz,
            'price': pc.price,
        }
        for pc in ProductColor.objects.select_related('product')
        .filter(product__categories__id=category_id)
    ]
