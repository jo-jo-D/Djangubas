import re

from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'supplier', 'price', 'quantity', 'article', 'available']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'category', 'supplier', 'price', 'quantity', 'article', 'available']


class ProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductDetail
        fields = ['product', 'description', 'manufacturing_date', 'expiration_date', 'weight']


class ProductDetailCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDetail
        fields = ['product', 'description', 'manufacturing_date', 'expiration_date', 'weight']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'house']


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_joined', 'deleted', 'deleted_at']
        read_only_fields = ['date_joined', 'deleted', 'deleted_at']


class CustomerCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_joined', 'deleted', 'deleted_at']

    def validate_phone_number(self, value):

        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError('Phone number must be 10-15 digits')
        if not value.isdigit():
            raise serializers.ValidationError('Phone number must be digit')

        # if not re.match(r'^\d{10,15}$', value):
        #     raise serializers.ValidationError('Phone number must be 10-15 digits')

        return value


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'order_date']
        read_only_fields = ['order_date']


class OrderCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['customer', 'order_date']
        read_only_fields = ['order_date']


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']


class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']


    def validate_quantity(self, value):
        if value > 1000:
            raise serializers.ValidationError('Quantity must be less than 1000')

        return value


class UserRegisterSerializer(serializers.ModelSerializer):
    # Делаем поле пароля только для записи (его нельзя будет прочитать из API)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
  # Используем create_user, чтобы пароль был правильно захеширован

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user















