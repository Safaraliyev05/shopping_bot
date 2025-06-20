from aiogram.types import InputMediaPhoto
from apps.models import Product, ProductImage, ProductColor, Cart, CartItem
from paginator import Paginator
from product_file.p_keyboard import get_product_keyboard


async def get_product_data(page: int = 1, per_page: int = 1, category_id=None):
    products = list(Product.objects.prefetch_related("images").all())
    if category_id:
        products = [p for p in products if category_id in p.categories.values_list('id', flat=True)]

    paginator = Paginator(products, page=page, per_page=per_page)
    page_products = paginator.get_page()
    if not page_products:
        return None, None

    product = page_products[0]
    image = product.images.first().image.path

    caption = f"<b>{product.name_uz}</b>\nNarxi: {product.colors.first().price} so'm\n" \
              f"<i>Sahifa {paginator.page} / {paginator.pages}</i>"

    keyboard = get_product_keyboard(
        level=2,
        category=category_id or 0,
        page=page,
        pagination_btns={"previous": paginator.has_previous(), "next": paginator.has_next()},
        product_id=product.id,
    )

    return image, caption, keyboard
