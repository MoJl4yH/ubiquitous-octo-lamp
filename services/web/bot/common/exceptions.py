"""
    Файл с кастомными исключениями.
"""


class AuthFailed(Exception):
    """ Исключение, которое вызывается при неудачной аутентификации. """

    def __init__(self, message: str = 'Authentication error') -> None:
        super().__init__(message)
