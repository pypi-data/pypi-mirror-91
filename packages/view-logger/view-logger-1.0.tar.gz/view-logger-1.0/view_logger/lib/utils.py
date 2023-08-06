from typing import Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser


def is_password(name: str) -> bool:
    """Метод проверяется, является переданный ключ паролем.

    Args:
        name (str): Ключ для проверки

    Returns:
        bool: Булевский результат сравнения
    """
    return name == 'password'


def too_long(value) -> bool:
    """Метод проверяет, является ли переданное значение слишком длинным.

    Args:
        value (any): Передаваемое значение на проверку

    Returns:
        bool: Результат проверки
    """
    return isinstance(value, str) and len(value) > 100


def user_info(user: Union[AbstractBaseUser, AnonymousUser]) -> str:
    """Метод подготавливает данные о пользователе для их логирования

    Args:
        info (Union): Информация о пользователе в неподготовленном виде.

    Returns:
        str: Подготовленная строка для логирования.
    """
    if user.is_anonymous:
        return '\n\t\t"Пользователь": \"Anonimus\",'
    return (
        f'\n\t\t"id": \"{user.id}\",'
        f'\n\t\t"Пользователь": \"{user.get_username()}\",'
        f'\n\t\t"Имя": \"{user.first_name} {user.last_name}\",'
        f'\n\t\t"email": \"{user.email}\",'
    )
