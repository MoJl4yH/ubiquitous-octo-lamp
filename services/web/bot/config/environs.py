import os
import logging

from ..common.classes import Environ


log = logging.getLogger(__name__)


# Определяем константы
ENV_PATH: str = '/app/config/.env'
# Переменные окружения, определяемые по умолчанию
DEFAULT_ENVS: tuple[Environ] = (
    Environ('YOUGILE_API_URL', 'https://yougile.com/api-v2'),
    Environ('TELEGRAM_API_URL', 'https://api.telegram.org/bot'),
    Environ('MESSAGES_PATH', '/app/config/messages.json'),
)
# Требуемые для самостоятельного ввода
REQUIRED_ENVS: tuple[Environ] = (
    Environ('BASE_URL', None),
    Environ('TELEGRAM_TOKEN', None),
    Environ('YOUGILE_TOKEN', None),
)


def add_environ(env: Environ) -> None:
    """ Инициализирует файл с переменными окружения, заносит в environ. """
    log.info('Запись в файл "%s"...', ENV_PATH)
    log.debug(
        'Сохраняем переменную окружения "%s" со значением "%s"',
        env.key, env.value
    )

    # Сразу же добавляем в environ
    os.environ[env.key] = env.value

    # Открываем и добавляем/записываем в файл
    with open(ENV_PATH, 'a+') as env_file:
        # Может быть проблема с предоставлением прав
        # для этого необходимо самостоятельно прописать права.

        # Записывать будем с учётом переноса строки
        # e.g. YOUGILE_API_URL=https://yougile.com/api-v2
        #      
        #      TELEGRAM_API_URL=https://api.telegram.org/bot
        env_file.write(f'\n{env.key}={env.value}')


def init_environs():
    """ Инициализация переменных окружения по-умолчанию """
    for env in DEFAULT_ENVS:
        if not os.getenv(env.key):
            add_environ(env)
