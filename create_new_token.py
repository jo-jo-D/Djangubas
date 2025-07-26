from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Получаем существующего пользователя (замените 'admin' на реальный логин)
try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    print("Пользователь не найден. Пожалуйста, создайте его.")
    exit() # Выходим, если пользователя нет

# Создаем токен для пользователя. get_or_create создает токен, если его нет.
token, created = Token.objects.get_or_create(user=user)

if created:
    print(f"Токен создан для пользователя {user.username}: {token.key}")
else:
    print(f"Токен уже существует для пользователя {user.username}: {token.key}")
