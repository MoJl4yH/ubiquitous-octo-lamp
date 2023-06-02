import os
import asyncio
import aiohttp
import logging
import requests

from typing import Sequence
from pydantic import parse_obj_as

from .classes import Response
from .exceptions import AuthFailed
from .models import BotCommand, BotCommandList


log = logging.getLogger(__name__)


# Константы
TELEGRAM_API_URL: str = os.environ.get('TELEGRAM_API_URL')
BASE_URL: str = os.environ.get('BASE_URL')
BOT_COMMANDS: tuple[BotCommand] = (
    BotCommand(command='start', description='начало'),
)


class TelegramRequester:
    """ Помогает создавать запросы к telegram API. """

    api_url: str = TELEGRAM_API_URL

    def __init__(self, token: str) -> None:
        self.__url = f'{self.api_url}{token}'
        self.session = aiohttp.ClientSession()

    @staticmethod
    async def check_response(resp):
        """ Проверяет ответ и оборачивает `result` в `Response`. """
        async with resp:
            # Что-то не то отправили
            if resp.status != 200:
                log.error(
                    'Невозможно отправить запрос "%s". Ошибка: %d',
                    resp.url, resp.status
                )
                log.info('Информация об ошибке: %s', str(await resp.json()))
                return Response(None, resp.status)

            # Пытаемся получить ответ
            try:
                json_data = await resp.json()
            except Exception as e:
                log.error('Невозможно получить json "%s": %s',
                          resp.url, str(e))
                return Response(None, resp.status)

        return Response(json_data.get('result'), resp.status)

    async def get(self, uri: str, params: dict = None) -> Response:
        """
            Отправляет GET HTTP запрос по uri с определёнными параметрами.

            Возвращает объект Response
          

        """
        # Отправляем запрос
        resp = await self.session.get(f'{self.__url}{uri}', params=params)
        return await self.check_response(resp)

    async def post(self, uri: str, data: dict = None) -> Response:
        """
            Отправляет POST HTTP запрос по uri с определёнными данными.

            Возвращает объект Response
            

        """
        # Отправляем запрос
        resp = await self.session.post(f'{self.__url}{uri}', json=data)
        return await self.check_response(resp)

    async def close(self):
        # Разрываем соединение

        await self.session.close()


class AsyncTelegramBot:
    """ Простой ассинхронный бот Telegram. """

    # Список команд бота по-умолчанию
    bot_commands: list[BotCommand] = list(BOT_COMMANDS)

    def __init__(self,
                 token: str,
                 use_bot_commands: bool = False,
                 bot_commands: Sequence[BotCommand] = None,
                 bot_commands_scope: str = 'all_private_chats') -> None:
        self.requester = TelegramRequester(token)
        self.use_bot_commands = use_bot_commands
        self.default_bot_commands_scope: str = bot_commands_scope

        # Меняем команды бота, если они пришли
        if bot_commands:
            self.bot_commands = bot_commands

        asyncio.get_event_loop().create_task(self.__config())

    async def __config(self) -> None:
        """ Запускает процесс конфигурации бота. """
        await self.delete_bot_commands()

        if self.use_bot_commands:
            await self.set_bot_commands(self.bot_commands)

    async def set_bot_commands(self,
                               bot_commands: Sequence[BotCommand],
                               scope_type: str = None):
        """ Добавляет `bot_commands` в список команд бота. """
        if not bot_commands:
            return

        if not scope_type:
            scope_type = self.default_bot_commands_scope

        # Список команд в dict
        commands: dict = BotCommandList(
            __root__=bot_commands
        ).dict()['__root__']

        # Подготавливаем данные
        data_to_send: dict = {
            'commands': commands,
            'scope': {'type': scope_type}
        }

        log.debug('Отправляем комманды в бота: %s', str(data_to_send))

        await self.requester.post('/setMyCommands', data=data_to_send)

    async def delete_bot_commands(self, scope_type: str = None) -> None:
        """ Удаляет команды бота. """
        scope_type = scope_type or self.default_bot_commands_scope

        log.debug('Очищаем команды бота в: %s', scope_type)

        await self.requester.post(
            '/deleteMyCommands',
            data={'scope': {'type': scope_type}}
        )

    async def init_bot_commands(self, scope_type: str = None) -> None:
        """
            Проверяет, что команды бота существуют
            (`по-умолчанию` или `commands` - TODO).

            В противном случае - вызывает `set_bot_commands()`

        """
        scope_type = scope_type or self.default_bot_commands_scope

        response: Response = await self.requester.post(
            '/getMyCommands', data={'scope': {'type': scope_type}}
        )
        if response.status != 200:
            log.error('Невозможно получить список команд бота...')
            return

        # Команды, которые уже существуют
        exist_commands: BotCommandList = BotCommandList(__root__=response.data)
        bot_commands_to_add: list[BotCommand] = []

        # Проходимся по командам бота
        for bot_command in self.bot_commands:
            # И добавляем незаписанные
            if bot_command not in exist_commands.__root__:
                bot_commands_to_add.append(bot_command)

        # Если необходимо добавить
        if bot_commands_to_add:
            log.debug('Нужно добавить в команды бота: %s', bot_commands_to_add)
            await self.set_bot_commands(
                bot_commands_to_add,
                scope_type=scope_type
            )

    async def send_message(self,
                           chat_id: int,
                           text: str,
                           reply_to_message_id: int = None,
                           parse_mode: str = None) -> dict:
        """ Отправляет сообщение, возвращает результат. """
        params = {
            'chat_id': chat_id,
            'text': text,
        }

        if reply_to_message_id:
            params['reply_to_message_id'] = reply_to_message_id
        if parse_mode:
            params['parse_mode'] = parse_mode

        response = await self.requester.get('/sendMessage', params=params)

        return response.data


def validate_telegram_token(token: str) -> bool:
    """ Проверяем telegram токен. """
    response = requests.get(f'{TELEGRAM_API_URL}{token}/getMe')
    return 200 == response.status_code


def resubscribe_webhook(token: str, url: str) -> None:
    """ Переподписываемся на вебхук... """
    # Удаляем (ничего не делаем) старую
    requests.get(f'{TELEGRAM_API_URL}{token}/deleteWebhook')
    requests.get(f'{TELEGRAM_API_URL}{token}/setWebhook?url={url}')


def check_subscription(token: str, url: str):
    """ Проверка существования подписки. """
    response = requests.get(f'{TELEGRAM_API_URL}{token}/getWebhookInfo')
    result = response.json().get('result', {})

    # Если не существует подписки или она отличается от текущего url
    if result.get('url') != url:
        resubscribe_webhook(token, url)


def telegram_webhook(token: str, url: str) -> None:
    """ Подписывает телеграм бота на вебхук. """
    check_subscription(token, f'{url}/telegram')
