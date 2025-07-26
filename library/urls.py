from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
# from .views import book_list_create, book_detail_update_delete
from .views import create_genre, BookListCreateView, BookDetailUpdateDeleteView, \
    ExpensiveBooksView, GenreDetailUpdateDeleteView, GenreViewSet, \
    books_by_date_view, lazy_load_demo, create_book_and_publisher_view

# urlpatterns = [
#     path('books/', book_list_create, name='book-list-create'),  # Для получения всех книг и создания новой книги
#     path('books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'),  # Для операций с одной книгой
# ]

router = DefaultRouter()

router.register('genres', GenreViewSet)

urlpatterns = [path('books/', BookListCreateView.as_view(), name='book-list-create'), # Для получения всех книг и создания новой книги
    path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-detail-update-delete'), # Для операций с одной книгой
    path('books/expensive/', ExpensiveBooksView.as_view(), name='book-expensive'),
    # path('genres/', create_genre, name='create-genre'), # Маршрут для создания жанра
    # path('genres/<str:name>/', GenreDetailUpdateDeleteView.as_view(), name='genre-detail-update-delete'),
    path('', include(router.urls)),
    re_path(r'^books/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', books_by_date_view, name='books-by-date'),
    path('lazy_load/', lazy_load_demo, name='lazy-load-demo'),
    path('books/transaction/', create_book_and_publisher_view, name='book-create-book-and-publisher'),
]