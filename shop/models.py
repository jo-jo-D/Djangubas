from django.db import models

class Category (models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.name}, {self.contact_email}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name='products')
    supplier = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    available_quantity = models.PositiveIntegerField()
    article = models.CharField(max_length=100, unique=True, db_index=True, help_text='Unique string product id')
    available = models.BooleanField(default=True)

    class Meta:
        ordering = [ 'category', 'quantity' ]

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='details')
    description = models.TextField(null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=False, blank=True, default='unlimited')
    weight = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)

    def __str__(self):
        return f"Description of {self.product.name}"



class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=6)

    def __str__(self):
        return f"Street: {self.street}, House: {self.house}"

    class Meta:
        verbose_name_plural = 'addresses'
        ordering = ['country', 'city']

class Customer(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, unique=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='customer')
    date_joined = models.DateField(auto_now_add=True, editable=False)


    class Meta:
        ordering = [ '-date_joined']
        get_latest_by = 'date_joined'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    order_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        ordering = [ '-order_date']
        get_latest_by = 'order_date'

    def __str__(self):
        return f"Order {self.id} by {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)


    def __str__(self):
        pass

    class Meta:
        ordering = [ '-order_date']
        get_latest_by = 'order_date'


