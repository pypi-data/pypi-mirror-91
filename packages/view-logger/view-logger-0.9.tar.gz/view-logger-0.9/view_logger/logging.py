import json
from functools import wraps
from logging import getLogger
from typing import Callable

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest

from .lib.utils import is_password, too_long, user_info

error_logger = getattr(settings, 'HTTP_ERROR_LOGGER', 'error_logger')
info_logger = getattr(settings, 'HTTP_INFO_LOGGER', 'info_logger')
user_object = getattr(settings, 'USER_OBJECT', 'user')


ERROR_LOGGER = getLogger(error_logger)
INFO_LOGGER = getLogger(info_logger)


def log_wrapper(func: Callable):
    """
    Декоратор для логирования необработанных ошибок.

    :param func: Функция для декорирования;

    :return: Декорированная функция.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            ERROR_LOGGER.error(f'\n\t\t"Error": "В функции {func.__name__} ошибка: {error}",')
            raise error

    return wrapper


def http_logger(func: Callable):
    """
    Декоратор для логирования HTTP запросов.

    :param func: Функция для декорирования;

    :return: Декорированная функция.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        def anonymize_token(token) -> str:
            if token is None:
                return 'Anonymous'
            return f'{token[:4]}....{token[-4:]}'

        def message(http_request) -> str:
            user: User = getattr(http_logger, user_object)
            user_agent = http_request.headers.get('User_agent', None)
            ip = http_request.META.get('HTTP_X_FORWARDED_FOR', 'None')
            user_token = http_request.headers.get('Authorization', None)

            body_info = ''
            if hasattr(http_request, 'body'):
                body_unicode = http_request.body.decode('utf-8')
                body = json.loads(body_unicode) if body_unicode else dict()
                for param_key in body:
                    value = body[param_key]
                    if too_long(value):
                        value = f'{value[0:99]}...'
                    if is_password(param_key):
                        value = '********'
                    body_info += f'\n\t\t\t{param_key}: {value}'

            if hasattr(http_request, 'GET'):
                query_params = dict(http_request.GET)
            else:
                query_params = dict()

            return (
                f'{user_info(user)}'
                f'\n\t\t"Агент клиента": "{user_agent}",'
                f'\n\t\t"ip": \"{ip.split(",", 1)[0]}\",'
                f'\n\t\t"token": "{anonymize_token(user_token)}",'
                f'\n\t\t"Запрос": "{http_request.path}",'
                f'\n\t\t"Метод": "{http_request.method}",'
                f'\n\t\t"Параметры": "{query_params}",'
                f'\n\t\t"Тело запроса": "{body_info}",'
                f'\n\t\t"Модуль": "{func.__module__}", "Функция": "{func.__name__}"'
            )

        request: HttpRequest = args[0]

        INFO_LOGGER.info(message(request))

        try:
            return func(*args, **kwargs)
        except Exception as error:
            ERROR_LOGGER.error(f'\n\t\t"Error": "{error}",{message(request)}')
            raise error

    return wrapper
