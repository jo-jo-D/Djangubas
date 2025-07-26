from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.serializers import ProductDetailCreateUpdateSerializer, OrderItemCreateUpdateSerializer
from shop.views import CategoryViewSet, SupplierViewSet, ProductListCreateView, ProductRetrieveUpdateDestroyView, \
    ProductDetailViewSet, AddressViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet, OrderStatisticsView, \
    LogoutView, LoginView, RegistrationView

# Создаем экземпляр роутера
router = DefaultRouter()

# Регистрируем наш ViewSet.
# 'category' - это префикс URL, по которому будут доступны наши категории.
# CategoryViewSet - представление, которое будет обрабатывать запросы.
router.register('category', CategoryViewSet)
router.register('supplier', SupplierViewSet)
router.register('product-detail', ProductDetailViewSet)
router.register('address', AddressViewSet)
router.register('customer', CustomerViewSet)
router.register('order', OrderViewSet, basename='order')
router.register('order-item', OrderItemViewSet)

# Основной список маршрутов нашего приложения.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListCreateView.as_view(), name='product-list-create'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('order-statistics/', OrderStatisticsView.as_view(), name='order-statistics'),
    path('login/', LoginView.as_view(), name='shop-login'),
    path('registration/', RegistrationView.as_view(), name='shop-registration'),
    path('logout/', LogoutView.as_view(), name='shop-logout'),
]