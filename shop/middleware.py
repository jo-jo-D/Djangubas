from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import resolve


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Пропускаем проверку для эндпоинтов, которые не требуют аутентификации
        if request.path_info in ['/shop/login/', '/shop/registration/', '/shop/logout/']:
            return

        access_token_cookie = request.COOKIES.get('access_token')

        # Если access_token есть в cookie, добавляем его в заголовок
        if access_token_cookie:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token_cookie}'

    def process_response(self, request, response):
        # Этот метод вызывается для КАЖДОГО ответа
        # Проверяем, был ли ответ с ошибкой "Token is invalid or expired"
        if response.status_code == 401 and b"Token is invalid or expired" in response.content:
            refresh_token_cookie = request.COOKIES.get('refresh_token')

            # Если есть refresh_token, пытаемся обновить access_token
            if refresh_token_cookie:
                try:
                    refresh = RefreshToken(refresh_token_cookie)
                    new_access_token = str(refresh.access_token)

                    # Если у нас есть новый refresh_token (из-за ротации), установим и его
                    if hasattr(refresh, 'access_token'):
                        new_refresh_token = str(refresh)
                        response.set_cookie('refresh_token', new_refresh_token, httponly=True, samesite='Lax',
                                            secure=False)  # secure=True в проде

                        # Устанавливаем новый access_token в cookie
                        response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax',
                                            secure=False)  # secure=True в проде

                        # Создаем новый запрос к исходному view, но уже с новым токеном
                        # Это позволяет "бесшовно" завершить исходный запрос пользователя
                        view, args, kwargs = resolve(request.path_info)
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                        kwargs['request'] = request
                        new_response = view(request, *args, **kwargs)

                        # Устанавливаем куки на новый ответ
                        new_response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax',
                                                secure=False)
                        if hasattr(refresh, 'access_token'):
                            new_response.set_cookie('refresh_token', new_refresh_token, httponly=True, samesite='Lax',
                                                    secure=False)

                        return new_response

                except TokenError:
                    # Если refresh_token тоже невалидный, удаляем cookie и ничего не делаем
                    response.delete_cookie('access_token')
                    response.delete_cookie('refresh_token')
                    # Возвращаем исходный ответ 401 Unauthorized
                    return response

        return response




