from datetime import datetime

from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, filters, mixins
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from django.db import reset_queries, connection, transaction

from .models import Book, Genre, Publisher
from .serializers import BookSerializer, BookDetailSerializer, BookCreateSerializer, GenreSerializer
from .permissions import IsOwnerOrReadOnly

class ReadOnlyOrAuthenticatedView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response({"message":"This is open to read for anyone, but modifications allowed only for authenticated users."})

    def post(self, request):
        return Response({"message":"Data created by authenticated user!"})


class AdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Greetings, Admin!"})

class PublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK, data={"message": "This endpoint is open for everyone"})

class ProtectedDataView(APIView):
    #   указываем, какие классы аутентификации использовать для этого представления
    #   здесь мы явно переопределяем или подтверждаем BasicAuthentication.

    # authentication_classes = [BasicAuthentication]

    #   если JWTAuthentication установлен как DEFAULT_AUTHENTICATION_CLASSES,
    #   здесь можно просто указать разрешения, а DRF сам проверит токен.

    #   указываем какие классы разрешений использовать.
    #   IsAuthenticated означает что только эти аут. имеют доступ
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #   если запрос дошел сюда, значит пользователь аутентифицирован и авторизирован
        #request.user теперь содержит объект пользователя
        return Response({"message": f"Hello, {request.user.username}!", "user": request.user.username})


# @api_view(['GET', 'POST'])
# def book_list_create(request):
#     if request.method == 'GET':
#         books = Book.objects.all()
#         serializer = BookListSerializer(books, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         serializer = BookCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BookListCreateView(APIView, PageNumberPagination):
#     page_size = 2
#
#     def get(self, request):
#         #### Filter ####
#         filters = {}
#         title = request.query_params.get('title')
#         published_year = request.query_params.get('pub_year')
#
#         if title:
#             filters['title'] = title
#
#         if published_year:
#             filters['publication_date__year'] = published_year
#
#         books = Book.objects.filter(**filters)
#
#         #### Sorting ####
#
#         # Получаем параметр 'sort_by'. Если его нет, по умолчанию сортируем по 'title'.
#         sort_by = request.query_params.get('sort_by', 'title')
#         # Получаем параметр 'sort_order'. По умолчанию сортируем по возрастанию ('asc').
#         sort_order = request.query_params.get('sort_order', 'asc')
#
#         if sort_order == 'desc': # Если порядок сортировки 'desc' (убывание)...
#             sort_by = f'-{sort_by}' # ...добавляем минус перед именем поля для убывающей сортировки
#         books = books.order_by(sort_by) # Применяем сортировку
#
#         #### Pagination ####
#
#         requested_page_size = self.get_page_size(request)
#         self.page_size = requested_page_size
#
#         result = self.paginate_queryset(books, request, view=self)
#
#         serializer = BookListSerializer(result, many=True)
#         return self.get_paginated_response(serializer.data)
#
#     def get_page_size(self, request):
#         page_size_param = request.query_params.get('page_size')
#
#         if page_size_param and page_size_param.isdigit():
#             return int(page_size_param)
#
#         return self.page_size
#
#     def post(self, request):
#         serializer = BookCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BookListCreateView(GenericAPIView):
#     # 1. Указываем, что мы работаем со всеми объектами модели Book
#     queryset = Book.objects.all()
#     # 2. Указываем, что для преобразования будем использовать BookSerializer
#     serializer_class = BookSerializer
#
#     # Метод для обработки GET-запроса (получение списка)
#     def get(self, request, *args, **kwargs):
#         # 1. Получаем набор всех книг с помощью встроенного метода
#         queryset = self.get_queryset()
#         # 2. Сериализуем набор объектов (many=True указывает, что объектов много)
#         serializer = self.get_serializer(queryset, many=True)
#         # 3. Возвращаем ответ в формате JSON
#         return Response(serializer.data)

#     # Метод для обработки POST-запроса (создание объекта)
#     def post(self, request, *args, **kwargs):
#         # 1. Передаем данные из запроса в сериализатор
#         serializer = self.get_serializer(data=request.data)
#         # 2. Проверяем, корректны ли данные. Если нет - вызовется исключение
#         serializer.is_valid(raise_exception=True)
#         # 3. Сохраняем новый объект в базу данных
#         serializer.save()
#         # 4. Возвращаем созданный объект и статус 201 CREATED
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# Этот класс заменяет наш BookListCreateView
# Он наследуется от ListCreateAPIView, который уже умеет:
# - обрабатывать GET для получения списка (List)
# - обрабатывать POST для создания объекта (Create)
class BookListCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    paginations_class = LimitOffsetPagination

    # Подключаем бэкенды для фильтрации, поиска и сортировки
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Поля, по которым можно будет точно фильтровать (author=...)
    filterset_fields = ['author', 'genres']

    # Поля, по которым будет работать полнотекстовый поиск (search=...)
    search_fields = ['title', 'description']

    # Поля, по которым можно будет сортировать (ordering=...)
    ordering_fields = ['publication_date', 'price']

    # Переопределяем метод create
    def create(self, request, *args, **kwargs):
        # Копируем данные из запроса, чтобы их можно было изменять
        data = request.data.copy()

        # Наша кастомная логика
        if 'author' not in data or not data['author']:
            data['author'] = 1

        # Дальше идет стандартная логика из DRF
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create вызывает serializer.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# # --- Представление для одного объекта (чтение, обновление, удаление) ---
# class BookDetailUpdateDeleteView(GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     # Метод для обработки GET-запроса (получение одного объекта)
#     def get(self, request, *args, **kwargs):
#         # 1. Получаем один конкретный объект по его pk (id) из URL
#         book = self.get_object()
#         # 2. Сериализуем его
#         serializer = self.get_serializer(book)
#         # 3. Возвращаем ответ
#         return Response(serializer.data)
#
#     # Метод для обработки PUT-запроса (полное обновление)
#     def put(self, request, *args, **kwargs):
#         book = self.get_object()
#         serializer = self.get_serializer(book, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     # Метод для обработки PATCH-запроса (частичное обновление)
#     def patch(self, request, *args, **kwargs):
#         book = self.get_object()
#         # partial=True говорит сериализатору, что обновление частичное
#         serializer = self.get_serializer(book, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     # Метод для обработки DELETE-запроса (удаление)
#     def delete(self, request, *args, **kwargs):
#         book = self.get_object()
#         book.delete()
#         # Возвращаем пустой ответ со статусом 204 NO CONTENT
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Этот класс заменяет наш BookDetailUpdateDeleteView
# Он наследуется от RetrieveUpdateDestroyAPIView, который умеет:
# - обрабатывать GET для получения одного объекта (Retrieve)
# - обрабатывать PUT/PATCH для обновления (Update)
# - обрабатывать DELETE для удаления (Destroy)
class BookDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]

    ## Переопределяем стандартный метод получения объекта
    # def get_object(self):
    #     # Сначала получаем pk из URL, как обычно
    #     pk = self.kwargs.get('pk')
    #
    #     try:
    #         # Ищем объект, который соответствует pk И НЕ является забаненным
    #         book = Book.objects.get(pk=pk, is_banned=False)
    #     except Book.DoesNotExist:
    #         # Если книга не найдена или забанена, вызываем ошибку 404
    #         raise NotFound(detail=f"Book with id '{pk}' not found or is banned.")
    #
    #     return book

    def get_serializer_context(self):
        # Получаем стандартный контекст
        context = super().get_serializer_context()
        # Добавляем в него наш флаг из параметров запроса
        context['include_related'] = self.request.query_params.get('include_related', 'false').lower() == 'true'
        return context


# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail_update_delete(request, pk):
#     try:
#         book = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = BookDetailSerializer(book)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'PUT':
#         serializer = BookCreateSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         book.delete()
#         return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# class BookDetailUpdateDeleteView(APIView):
#     def get(self, request, pk):
#         try:
#             book = Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = BookDetailSerializer(book)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         try:
#             book = Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = BookCreateSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             book = Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ExpensiveBooksView(ListAPIView):
    serializer_class = BookSerializer

    # Мы не указываем queryset, т.к. будем формировать его динамически
    # Вместо этого мы полностью переопределяем метод get_queryset
    def get_queryset(self):
        # 1. Вычисляем среднюю цену всех книг
        average_price = Book.objects.aggregate(avg_price=Avg('price'))['avg_price']

        if average_price is None:
            return Book.objects.none()  # Возвращаем пустой набор, если книг нет

        # 2. Возвращаем книги, цена которых выше средней
        return Book.objects.filter(price__gt=average_price)


@api_view(['POST'])
def create_genre(request):
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # Возвращаем ошибки, если данные некорректны
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    # Говорим DRF искать объект по полю 'name' в модели Genre
    lookup_field = 'name'

    # Этот атрибут не обязателен, если имя в URL совпадает с lookup_field,
    # но для ясности лучше его указать.
    lookup_url_kwarg = 'name'


# class GenreReadOnlyView(ReadOnlyModelViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#
# class GenreListRetrieveUpdateViewSet(mixins.ListModelMixin,
#                                      mixins.RetrieveModelMixin,
#                                      mixins.UpdateModelMixin,
#                                      GenericViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    # Наш новый кастомный метод
    @action(detail=False, methods=['get'])
    def statistic(self, request):
        """
        Возвращает количество книг для каждого жанра.
        """
        # С помощью annotate добавляем к каждому жанру поле book_count
        genres_with_book_counts = Genre.objects.annotate(book_count=Count('books'))

        # Формируем данные для ответа
        data = [
            {
                "id": genre.id,
                "genre": genre.name,
                "book_count": genre.book_count
            }
            for genre in genres_with_book_counts
        ]
        return Response(data)


@api_view(['GET'])
def books_by_date_view(request, year=None, month=None, day=None):
    # Django автоматически передает захваченные 'year', 'month', 'day' в функцию
    books = Book.objects.filter(publication_date__year=year,
                                publication_date__month=month,
                                publication_date__day=day)
    serializer = BookSerializer(books, many=True)

    return Response({'date': f"{year}-{month}-{day}", 'books': serializer.data})


@api_view(['GET'])
def lazy_load_demo(request):
    # Endpoint for testing lazy load

    reset_queries()

    # Этот код ОЧЕНЬ НЕЭФФЕКТИВЕН!
    # books = Book.objects.all()  # 1-й запрос: получить ВСЕ книги

    # Оптимизация с помощью select_related
    books = Book.objects.select_related('publisher').all()  # Всего ОДИН запрос!

    print(connection.queries)

    for book in books:
        # Для КАЖДОЙ книги делается ОТДЕЛЬНЫЙ запрос к БД, чтобы получить издателя
        print(book.publisher.name)  # N дополнительных запросов

    print(connection.queries)

    print("#" * 100)

    reset_queries()

    # Оптимизация с помощью prefetch_related
    books = Book.objects.prefetch_related('genres').all()  # Всего ДВА запроса!

    for book in books:
        print("Книга:", book.title)
        # Доступ к book.genres.all() теперь не вызывает новых запросов
        for genre in book.genres.all():
            print("  - Жанр:", genre.name)

    print(connection.queries)

    print("#" * 100)

    reset_queries()

    books = Book.objects.select_related('publisher').prefetch_related('genres').all()  # Все еще 2 запроса!

    for book in books:
        print("Книга:", book.title)
        print(book.publisher.name)
        # Доступ к book.genres.all() теперь не вызывает новых запросов
        for genre in book.genres.all():
            print("  - Жанр:", genre.name)

    print(connection.queries)

    return Response({'data': 'success'})


@api_view(['POST'])
def create_book_and_publisher_view(request):
    try:
        # Все, что находится внутри этого блока, — одна транзакция
        with transaction.atomic():
            # 1. Создаем издателя
            publisher = Publisher.objects.create(name="Super Publisher", established_date=datetime.now())

            # Искусственно создадим ошибку, чтобы проверить откат
            if not request.data.get('title'):
                raise ValueError("Название книги обязательно!")

            # 2. Создаем книгу
            # Этот код не выполнится, если возникнет ошибка выше
            book = Book.objects.create(
                title=request.data.get('title'),
                publisher=publisher
            )
        # Если блок with завершился без ошибок, транзакция фиксируется (commit)

    except Exception as e:
        # Если внутри блока with произошла любая ошибка,
        # все изменения в БД (создание Publisher) будут отменены (rollback).
        return Response({'error': str(e)}, status=400)

    return Response({'status': 'Book and Publisher created'})


@api_view(['POST'])
@transaction.atomic  # Декоратор применяет транзакцию ко всей функции
def create_book_and_publisher_view(request):
    try:
        # 1. Создаем издателя
        publisher = Publisher.objects.create(name="Super Publisher")

        # 2. Создаем книгу
        book = Book.objects.create(
            title="A New Book",
            publisher=publisher
        )

        # ... другая логика ...

    except Exception as e:
        # Если здесь произойдет ошибка, вся транзакция будет отменена
        # и ни книга, ни издатель не будут сохранены в БД.
        return Response({'error': str(e)}, status=400)

    serializer = BookSerializer(book)
    return Response(serializer.data)


@api_view(['POST'])
@transaction.atomic  # Декоратор применяет транзакцию ко всей функции
def create_book_and_publisher_view(request):
    try:
        # 1. Создаем издателя
        publisher = Publisher.objects.create(name="Super Publisher")

        # 2. Создаем книгу
        book = Book.objects.create(
            title="A New Book",
            publisher=publisher
        )

        # ... другая логика ...

    except Exception as e:
        # Если здесь произойдет ошибка, вся транзакция будет отменена
        # и ни книга, ни издатель не будут сохранены в БД.
        return Response({'error': str(e)}, status=400)

    serializer = BookSerializer(book)
    return Response(serializer.data)