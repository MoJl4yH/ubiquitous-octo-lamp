"""
    Файл с полезными штуками.

    Например, дата классы для запросов/ответов, enum`ы

"""


from dataclasses import dataclass
from enum import Enum


@dataclass
class Response:
    '''
        Структура для хранения результата ответа.
    '''

    data: dict
    status: int


@dataclass
class ResultEntity:
    """ Структура хранения сущности состояния. """
    code: int = 0
    message: str = None
    data: dict = None


@dataclass
class Error(ResultEntity):
    """ Структура хранения ошибки. """


@dataclass
class Ok(ResultEntity):
    """ Структура хранения успеха. """


@dataclass
class Result:
    """ Структура для хранения результатов выполнения. """
    ok: Ok = None
    error: Error = None


@dataclass
class Environ:
    '''
        Структура для хранения переменной окружения.
    '''
    key: str
    value: str


class UserState(Enum):
    """ Enumerate состояний пользователя """
    START = 0
    WAITING_EMAIL = 1
    READY = 2


@dataclass
class UserInfo:
    """ Структура, хранящаяя данные о пользователе """
    user_id: int
    yougile_id: str
    state: UserState
    is_changed: bool = False
