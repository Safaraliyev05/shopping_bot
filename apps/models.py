from django.db.models import Model, BigIntegerField, CharField, BooleanField, ForeignKey, CASCADE, ManyToManyField, \
    ImageField, OneToOneField, PositiveIntegerField, DateTimeField, DecimalField


class User(Model):
    telegram_id = BigIntegerField(unique=True)
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    language = CharField(max_length=2, choices=[('uz', 'Uzbek'), ('ru', 'Russian')], default='uz')
    is_blocked = BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"


class Category(Model):
    parent = ForeignKey('self', null=True, blank=True, on_delete=CASCADE, related_name='subcategories')
    name_uz = CharField(max_length=255)
    name_ru = CharField(max_length=255)

    def __str__(self):
        return self.name_uz


class Product(Model):
    name_uz = CharField(max_length=255)
    name_ru = CharField(max_length=255)
    categories = ManyToManyField(Category, related_name='products')
    main_image = ImageField(upload_to='products/')

    def __str__(self):
        return self.name_uz


class ProductColor(Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name='colors')
    color_name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name_uz} - {self.color_name}"


class ProductColorImage(Model):
    product_color = ForeignKey(ProductColor, on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='product_colors/')

    def __str__(self):
        return f"{self.product_color}"


class Cart(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='cart')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name}'s Cart"


class CartItem(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name='items')
    product_color = ForeignKey(ProductColor, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_color} x{self.quantity}"


class Order(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='orders')
    created_at = DateTimeField(auto_now_add=True)
    is_completed = BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.user.full_name}"


class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='items')
    product_color = ForeignKey(ProductColor, on_delete=CASCADE)
    quantity = PositiveIntegerField()

    def __str__(self):
        return f"{self.product_color} x{self.quantity}"
