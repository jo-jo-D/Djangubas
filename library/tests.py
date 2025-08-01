from django.test import TestCase
from rest_framework.test import APITestCase

import pytest
from .models import SimpleBook

# Пометка, которая говорит pytest, что этот тест может работать с базой данных
@pytest.mark.django_db
def test_simple_book_model():
    """
    Тест для проверки создания объекта книги и работы кастомного метода is_classic().
    """
    # 1. Arrange (Подготовка): Создаем объект в памяти
    book = SimpleBook.objects.create(
        title="Война и мир",
        author="Лев Толстой",
        publication_year=1869
    )

    # 2. Act (Действие) & Assert (Проверка)
    # Проверяем, что объект создался и его поля соответствуют ожидаемым
    assert book.title == "Война и мир"
    assert str(book) == "Война и мир" # Проверяем работу метода __str__