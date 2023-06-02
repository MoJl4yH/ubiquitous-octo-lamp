import os
import aiohttp
import logging
import requests

from datetime import datetime

from .classes import Response
from .exceptions import AuthFailed


log = logging.getLogger(__name__)


# Константы
YOUGILE_API_URL: str = os.getenv('YOUGILE_API_URL')


class YouGileRequester:
    """ Помогает создавать запросы к YouGile API. """

    __url: str = YOUGILE_API_URL

    def __init__(self, token: str) -> None:
        self.__headers = {'Authorization': f'Bearer {token}'}

    @staticmethod
    async def check_response(resp, expected_status: int = 200):
        """ Проверяет ответ и оборачивает `content` в `Response`. """
        async with resp:
            # Что-то не то отправили
            if resp.status != expected_status:
                log.error(
                    'Невозможно отправить запрос "%s". Ошибка: %d',
                    resp.url, resp.status
                )
                return Response(None, resp.status)

            # Пытаемся получить ответ
            try:
                json_data = await resp.json()
            except Exception as e:
                log.error('Невозможно получить json "%s": %s',
                          resp.url, str(e))
                return Response(None, resp.status)

        # Проверяем content, включая content = []
        if 'content' in json_data:
            json_data = json_data['content']
        
        return Response(json_data, resp.status)

    async def get(self, uri: str, params: dict = None) -> Response:
        """
            Отправляет `GET HTTP` запрос по uri с определёнными параметрами.

            Возвращает объект `Result`

        """
        # Открываем сессию
        async with self.__get_session() as session:
            # Отправляем запрос
            resp = await session.get(f'{self.__url}{uri}?limit=1000',
                                     params=params)

        return await self.check_response(resp, 200)

    def __get_session(self):
        return aiohttp.ClientSession(headers=self.__headers)

    async def post(self, uri: str, data: dict = None) -> Response:
        """
            Отправляет `POST HTTP` запрос по uri с определёнными данными.

            Возвращает объект `Response`

        """
        # Открываем сессию
        async with self.__get_session() as session:
            # Отправляем запрос
            resp = await self.session.post(f'{self.__url}{uri}', json=data)

        return await self.check_response(resp, 201)



class Authenticator:
    """ Синхронно получает YouGile токен. """

    url = YOUGILE_API_URL

    def __init__(self, login: str, password: str):
        response = requests.post(
            f'{self.url}/auth/companies',
            data={'login': login, 'password': password}
        )

        # Если невозможно зайти по кредам
        if response.status_code != 200:
            raise AuthFailed('Неправильный логин или пароль...')

        self.__login_data = {'login': login, 'password': password}

    def get_companies(self, company_name: str = '', offset: int = 0,
                      limit: int = 50) -> list:
        """ Получаем список компаний с помощью YouGile API. """
        response = requests.post(
            f'{self.url}/auth/companies?offset={offset}&limit={limit}',
            data={**self.__login_data, 'name': company_name}
        )

        # Проблема с запросом
        if response.status_code != 200:
            log.error('Ошибка в запросе получения списка компаний: %d',
                      response.status_code)
            return None

        #  Получение списка компаний
        try:
            companies: list = response.json()['content']
        except Exception as e:
            log.error('Ошибка в получении списка компаний: %s', str(e))
            return None

        return companies

    def get_token(self, company_id: str) -> str:
        """ Получение токена. """
        response = requests.post(
            f'{self.url}/auth/keys',
            data={**self.__login_data, 'companyId': company_id}
        )
        status: int = response.status_code

        if status != 201:
            log.error('Ошибка в запросе на получение ключа: %d', status)
            return None

        # Хардкодим получение токена
        try:
            key: str = response.json()['key']
        except Exception as e:
            log.error('Невозможно получить ключ: %s', str(e))
            return None

        return key


def resubscribe_webhook(headers: dict, url: str) -> None:
    """ Переподписываемся на вебхуку... """
    requests.post(f'{YOUGILE_API_URL}/webhooks', headers=headers, data={
        'url': f'{url}',
        'event': 'task-*',
    })


def check_subscription(headers: dict, url: str) -> None:
    """ Проверка существования подписки. """
    response = requests.get(f'{YOUGILE_API_URL}/webhooks', headers=headers)
    subscriptions: list = response.json()

    # ... Просто перебираем подписки
    sub_counter = 0
    for subscription in subscriptions:
        if subscription['url'] == url:
            sub_counter += 1

    # Если в списке нет подписки
    if not sub_counter:
        resubscribe_webhook(headers, url)


def yougile_webhook(token: str, url: str) -> None:
    """ Подписываемся на YouGile вебхук. """
    headers = {'Authorization': f'Bearer {token}'}
    check_subscription(headers, f'{url}/yougile')
