from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Category, Supplier
from shop.permissions import IsOwnerOrReadOnly, CanViewOrderStatistics
from shop.serializers import *


# Вспомогательная функция для установки cookie
def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True, secure=False, samesite='Lax'
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True, secure=False, samesite='Lax'
    )


class LoginView(APIView):
    # Разрешаем доступ всем (даже анонимным пользователям), чтобы они могли войти
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Проверяем, существует ли пользователь с таким логином и паролем
        user = authenticate(request, username=username, password=password)

        if user:
            # Создаем успешный ответ
            response = Response(status=status.HTTP_200_OK)
            set_jwt_cookies(response, user)
            return response
        else:
            return Response()

            # ВЫНЕСЛИ В ОТДЕЛЬНУЮ ФУНКЦИЮ
            # # Если пользователь найден, создаем для него токены
            # refresh = RefreshToken.for_user(user)
            # access_token = refresh.access_token
            #
            #
            # # Устанавливаем access_token в cookie
            # response.set_cookie(
            #     key='access_token',
            #     value=str(access_token),
            #     httponly=True,  # Защита от доступа через JavaScript
            #     secure=False,   # В продакшене должно быть True (только для HTTPS)
            #     samesite='Lax'
            # )
            # # Устанавливаем refresh_token в cookie
            # response.set_cookie(
            #     key='refresh_token',
            #     value=str(refresh),
            #     httponly=True,
            #     secure=False,   # В продакшене должно быть True
            #     samesite='Lax'
            # )\

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Создаем ответ с данными пользователя
            response = Response({
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)

            # Вызываем нашу функцию, чтобы добавить cookie с токенами в ответ
            set_jwt_cookies(response, user)
            return response

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        # Создаем пустой ответ
        response = Response(data={'message': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)

        # Отправляем команду браузеру на удаление cookie
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Это представление предоставляет полный набор действий (CRUD) для модели Category.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SupplierViewSet(viewsets.ModelViewSet):
    """
    Это представление предоставляет полный набор действий (CRUD) для модели Supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ProductListCreateView(ListCreateAPIView):
    """
    Представление для получения списка продуктов и создания нового продукта.
    """
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price']

    # Явно указываем классы аутентификации для этого представления.
    # Это переопределит глобальные настройки, если они есть.
    # authentication_classes = [BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]

    # Явно указываем классы разрешений для этого представления.
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Этот метод позволяет нам динамически выбирать сериалайзер
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких как GET
        if self.request.method == 'GET':
            return ProductSerializer
        # Для остальных методов (POST)
        return ProductCreateUpdateSerializer


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления одного продукта.
    """
    queryset = Product.objects.all()

    # Явно указываем классы разрешений для этого представления.
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        # Для чтения данных
        if self.request.method == 'GET':
            return ProductSerializer
        # Для изменения или удаления (PUT, PATCH, DELETE)
        return ProductCreateUpdateSerializer


class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    # Явно указываем классы разрешений для этого представления.
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Этот метод позволяет нам динамически выбирать сериалайзер
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких как GET
        if self.request.method == 'GET':
            return ProductDetailSerializer
        # Для остальных методов
        return ProductDetailCreateUpdateSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    # Явно указываем классы разрешений для этого представления.
    permission_classes = [IsAdminUser]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

    # Явно указываем классы разрешений для этого представления.
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerSerializer
        return CustomerCreateUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    # Явно указываем классы разрешений для этого представления.
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Этот метод определяет список объектов для отображения.
        Мы фильтруем заказы, оставляя только те, где поле `user`
        совпадает с текущим пользователем.
        Таким образом, каждый пользователь видит только свои заказы.
        """
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        return OrderCreateUpdateSerializer

    # Переопределяем метод perform_create
    def perform_create(self, serializer):
        """
        При создании заказа мы автоматически подставляем текущего пользователя
        в поле `user`. `self.request.user` — это и есть текущий
        авторизованный пользователь.
        """
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()

    # Явно указываем классы разрешений для этого представления.
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderItemSerializer
        return OrderItemCreateUpdateSerializer


class OrderStatisticsView(APIView):
    # Применяем наше новое разрешение и IsAuthenticated
    permission_classes = [IsAuthenticated, CanViewOrderStatistics]

    def get(self, request):
        total_orders = Order.objects.count()
        data = {
            'total_orders': total_orders,
        }
        return Response(data)
