import os
import getpass
import logging

from ..common.exceptions import AuthFailed
# TODO: мне не нравится этот колхоз
from .environs import init_environs, add_environ, ENV_PATH, REQUIRED_ENVS


log = logging.getLogger(__name__)


# Инициализация
try:
    init_environs()
except PermissionError:
    log.critical('Невозможно создать файл "%s"...', ENV_PATH)
    log.info('Требуется дать разрешение на запись...')
    exit(1)


from ..common.yougile import Authenticator, yougile_webhook
from ..common.telegram import validate_telegram_token, telegram_webhook


def get_telegram_token() -> str:
    """ Получаем telegram токен. """
    log.warning('В файле "%s" нет telegram токена...', ENV_PATH)
    log.info(
        'Telegram токен можно узнать/создать в официальном боте: @BotFather'
    )

    # Бесконечный цикл, пока пользователь не введёт правильный токен
    token = input('Введите telegram токен: ')
    while not validate_telegram_token(token):
        log.error('Недействительный токен')
        token = input('Введите telegram токен: ')

    return token


def get_yougile_auth() -> Authenticator:
    """ Возвращает аутентификатор с кредами пользователя. """
    login = input('Логин YouGile: ')
    password = getpass.getpass('Пароль (скрыт): ')

    try:
        return Authenticator(login, password)
    except AuthFailed as e:
        log.error(e)
        return None


def get_company_number(current: str, companies_len: int) -> int:
    """
        Просто хэлпер, который поможет сократить луп.

        Возвращает номер, если введённое с клавы содержится в списке компаний.

    """
    if not current.isdigit() or int(current) < 1 or \
            int(current) > companies_len:
        return None

    return int(current) - 1


def get_yougile_token() -> str:
    """ Получаем YouGile токен. """
    log.warning('В файле "%s" нет YouGile токена...', ENV_PATH)
    log.info('YouGile токен можно получить, введя креды и выбрав компанию')

    # Бесконечный цикл, пока пользователь не введёт правильные креды
    auth: Authenticator = get_yougile_auth()
    while not auth:
        auth = get_yougile_auth()

    log.info('Вход успешно произведён...')

    # Получаем список компаний
    companies: list = auth.get_companies()
    if not companies:
        log.critical('У вас нет ни одной компани...')
        exit(1)

    log.info('Список доступных компаний:')
    for i, company in enumerate(companies):
        log.info(f"[{i + 1}] {company.get('name', 'Нет названия')}")

    # Бесконечный цикл, пока пользователь вводит неправильный номер компании
    company_num = None
    while company_num is None:
        user_input: str = input('Выберите номер компании [в скобках]: ')
        company_num: int = get_company_number(user_input, len(companies))

    # Ну уж id должен быть... или нет...
    company_id = companies[company_num]['id']
    company_token = auth.get_token(company_id)
    if not company_token:
        # ...
        log.critical('Ошибка в получении токена...')
        exit(1)

    return company_token


def get_base_url() -> str:
    """ Получаем домен нашего сервера. """
    # TODO: переписать
    log.warning('В файле "%s" нет BASE_URL...', ENV_PATH)
    log.info('Требуется полный домен сервера (e.g. https://google.com)...')

    base_url = None
    while not base_url:
        base_url = input('Введите полный домен сервера: ')

    return base_url


# Проверяем переменные окружения по-умолчанию
for env in REQUIRED_ENVS:
    # Если значение установлено
    if os.getenv(env.key):
        # Пропускаем
        continue

    match env.key:
        case 'TELEGRAM_TOKEN':
            env.value = get_telegram_token()
        case 'YOUGILE_TOKEN':
            env.value = get_yougile_token()
        case 'BASE_URL':
            env.value = get_base_url()

    # Пробуем записать в файл
    try:
        add_environ(env)
    except PermissionError:
        log.critical('Невозможно создать файл "%s"...', ENV_PATH)
        log.info('Требуется дать разрешение на запись...')
        exit(1)

# Подписываемся на вебхуки
telegram_webhook(os.environ['TELEGRAM_TOKEN'], os.environ['BASE_URL'])
yougile_webhook(os.environ['YOUGILE_TOKEN'], os.environ['BASE_URL'])


