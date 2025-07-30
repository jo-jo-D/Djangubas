from django.contrib.auth.models import User
from django.db import models
from itertools import product

from HomeDjangubas import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    article = models.CharField(max_length=100, unique=True, help_text="Unique string product id", db_index=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = [ 'category', 'name']

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='details')
    description = models.TextField(null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Details of {self.product.name}"


class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=6)

    def __str__(self):
        return f"Street: {self.street}, House: {self.house}"

    class Meta:
        verbose_name_plural = 'addresses'


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer')
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_joined']
        get_latest_by = 'date_joined'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        related_name='orders'
    )

    class Meta:
        ordering = ['-order_date']
        get_latest_by = 'order_date'

        # Добавляем кастомное разрешение
        permissions = [
            ("can_view_order_statistics", "Can view order statistics"),
        ]


    def __str__(self):
        return f"Order {self.id} by {self.customer}"     # self.customer -- Здесь автоматически подхватит return f"{self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    # Количество заказанного продукта/товара:
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product} for {self.order}"