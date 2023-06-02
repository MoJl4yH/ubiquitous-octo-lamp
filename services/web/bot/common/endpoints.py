import os
import asyncio
import logging

from .yougile import YouGileRequester
from .messages import DEFAULT_MESSAGES, yougile_task_to_text
from .validators import is_valid_email
from .telegram import AsyncTelegramBot
from .classes import UserInfo, UserState, Result, Error, Ok
from .models import User, YouGileTask, BotCommand, Message


# Константы
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
YOUGILE_TOKEN = os.environ['YOUGILE_TOKEN']
BOT_COMMANDS: tuple[BotCommand] = (
    BotCommand(command='start', description='начало'),
    BotCommand(command='help', description='помощь'),
    BotCommand(command='change_email', description='поменять email'),
    BotCommand(command='stop', description='отписаться от задач'),
)


log = logging.getLogger(__name__)
bot = AsyncTelegramBot(
    token=TELEGRAM_TOKEN,
    use_bot_commands=True,
    bot_commands=BOT_COMMANDS
)
yougile_requester = YouGileRequester(YOUGILE_TOKEN)


# Подтверждённые пользователи (id YouGile известен)
real_users: dict[str, int] = {}


async def telegram_start(user: User) -> None:
    """ Отправляет приветственное сообщение. """
    message: str = DEFAULT_MESSAGES['hello'].safe_substitute(
        user_name=user.first_name
    )

    await bot.send_message(user.id, message, parse_mode='MarkdownV2')


async def telegram_help(user: User):
    """ Отправляет инструкциию по работе с ботом. """
    message: str = DEFAULT_MESSAGES['help'].safe_substitute()
    await bot.send_message(user.id, message, parse_mode='MarkdownV2')


async def telegram_reminder(user: User):
    """ Отправляет напоминание, что нужно отправить почту """
    message: str = DEFAULT_MESSAGES['email_waiting'].safe_substitute()
    await bot.send_message(user.id, message, parse_mode='MarkdownV2')


async def new_yougile_event(event: str, task: YouGileTask):
    """ Получает новую задачу и распределяет между пользователями. """
    message_text: str = yougile_task_to_text(
        task=task,
        event=event.split('-')[-1]
    )
    # Наши асинхронные задачи
    async_tasks = []

    # Получаем список пользователей, которым будет отправлена задача
    # Если список исполнителей пустой - делаем всех исполнителями
    if not task.assigned:
        task.assigned = real_users.keys()

    # Если task.assigned - строка, делаем список
    if isinstance(task.assigned, str):
        task.assigned = [task.assigned]

    # Для каждого YouGile id из списка исполнителей
    for yougile_id in task.assigned:
        # Получаем telegram id из yougile id
        user_id = real_users.get(yougile_id)
        # Планируем отправлять только существующим пользователям в telegram
        if user_id:
            async_tasks.append(bot.send_message(
                user_id,
                message_text,
                parse_mode='MarkdownV2'
            ))

    # Отправляем задачи на выполнение
    await asyncio.gather(*async_tasks)


def result_error(message: str = None, code: int = 0) -> Result:
    """ Возвращает ошибочный результат. """
    return Result(error=Error(code=int, message=message))


def result_ok(message: str = None, code: int = 0, data: dict = None) -> Result:
    """ Возвращает положительный результат. """
    return Result(ok=Ok(code=int, message=message, data=data))


def restart_session(user_info: UserInfo) -> UserInfo:
    """
        Очищает `real_users` от `user_info`.`user_id`,
        также удаляет `yougile_id` из `user_info` и меняет состояние на `START`
    """
    user_info.state = UserState.START
    if user_info.yougile_id in real_users:
        del real_users[user_info.yougile_id]
    if user_info.yougile_id:
        user_info.yougile_id = None

    log.debug(user_info)
    return user_info


async def change_user_email(message_id: int, user_info: UserInfo) -> UserInfo:
    """
        Запуск процесса изменения email.

        Меняет `real_users`, `user_info`.`state` и отправляет сообщение

    """
    # Если пользователь не проходил процесс проверки почты
    if not user_info.yougile_id:
        message_to_send = DEFAULT_MESSAGES['no_email'].safe_substitute()
    else:
        message_to_send = DEFAULT_MESSAGES['email_change'].safe_substitute()

    # Отправляем сообщение
    await bot.send_message(user_info.user_id, message_to_send,
                           reply_to_message_id=message_id)

    return restart_session(user_info)


async def yougile_get_user_id_by_email(email: str) -> Result:
    """
        Если `email` содержится в компании, возвращает `Result`
        с `yougile_id` пользователя.

        При ошибке возвращает `Result`.`error` с текстом
    """
    # Если почта не прошла проверку
    if not is_valid_email(email):
        # Готовим сообщение, что почта неправильная
        error_message = DEFAULT_MESSAGES['email_not_valid'].safe_substitute(
            email=email
        )
        # Возвращаем результат
        return result_error(message=error_message)

    # Отправляем запрос с присланной почтой
    response = await yougile_requester.get('/users', params={'email': email})
    # Если вернулась пустота
    if not response.data:
        # Отправляем сообщение с ошибкой
        error_message = DEFAULT_MESSAGES['email_error'].safe_substitute()
        return result_error(message=error_message)

    # Возвращаем успех с сообщением и данными пользователя
    ok_message = DEFAULT_MESSAGES['email_correct'].safe_substitute()
    return result_ok(message=ok_message, data=response.data[0])



async def additional_commands(message: Message,
                              user_info: UserInfo) -> UserInfo:
    """
        По идее, здесь должно происходить перенаправление
        незакреплённых команд, например, получение почты и т.д.
    """
    # Вызываем необходимую функцию исходя из состояния пользователя
    match user_info.state:
        # Пользователь вводит почту
        case UserState.WAITING_EMAIL:
            result: Result = await yougile_get_user_id_by_email(
                email=message.text.lower()
            )
            # Получили успех
            if result.ok:
                # Отправляем сообщение, что всё ок
                await bot.send_message(
                    chat_id=user_info.user_id,
                    text=result.ok.message,
                    reply_to_message_id=message.message_id,
                    parse_mode='MarkdownV2'
                )
                # Добавляем пользователя в подтверждённые
                real_users[result.ok.data['id']] = user_info.user_id
                # Меняем состояние на "ГОТОВ"
                user_info.state = UserState.READY
                # Добавляем yougile id
                user_info.yougile_id = result.ok.data['id']
        # Пользователь в состоянии "ГОТОВ"
        case UserState.READY:
            return user_info
        # У пользователя не установлено состояние
        case _:
            # Отправляем "привет"
            await telegram_start(message.from_user)
            return user_info

    # Если в результате получили ошибку
    if result.error:
        # Отправляем сообщение с текстом ошибки
        await bot.send_message(
            chat_id=user_info.user_id,
            text=result.error.message,
            reply_to_message_id=message.message_id,
            parse_mode='MarkdownV2'
        )

    return user_info


async def state_proccessor(user: User, user_info: UserInfo):
    """ Обработка состояний (не стадий принятия!) пользователей. """
    user_info_changed = False

    # Обрабатываем состояния
    match user_info.state:
        # Пользователь должен ввести почту
        case UserState.WAITING_EMAIL:
            await telegram_reminder(user)
        # Пользователь со стартовым состоянием
        case UserState.START:
            log.debug(user_info)
            user_info.state = UserState.WAITING_EMAIL
            user_info_changed = True
        # Что-то странное
        case _:
            ...

    # Должны дать знать, если поменяли что-то
    user_info.is_changed = user_info_changed

    return user_info
