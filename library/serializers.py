from rest_framework import serializers
from django.utils import timezone
from .models import Book, Publisher, Genre
from .validators import validate_title_length


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookCreateSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(read_only=True)
    title = serializers.CharField(validators=[validate_title_length])
    pages = serializers.IntegerField()
    publisher = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Publisher.objects.all()
    )

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['created_at', 'id']

    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            validated_data['title'] = validated_data['title'].strip().title()

        return super().update(instance, validated_data)

    def validate_pages(self, value):
        if value < 1:
            raise serializers.ValidationError('Amount of pages cant be less then 1.')
        return value

    def validate(self, data):
        if data.get('discounted_price') and data.get('price'):
            if data['discounted_price'] > data['price']:
                raise serializers.ValidationError('Discounted price cant be higher then regular price.')

        return data


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        # Получаем стандартное представление объекта
        representation = super().to_representation(instance)

        # Проверяем флаг, который мы передали из представления
        if not self.context.get('include_related'):
            # Если флаг false, удаляем поле 'genres' из ответа
            representation.pop('genres', None)

        return representation


class BookDetailSerializer(serializers.ModelSerializer):
    # publisher = PublisherSerializer()
    # publisher = serializers.StringRelatedField()

    # publisher = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Publisher.objects.all()
    # )

    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'