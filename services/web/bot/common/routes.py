import logging

from fastapi import Request

from .. import app
from .classes import UserInfo, UserState
from .models import TelegramUpdate, YouGileTaskUpdate

from .endpoints import telegram_start, telegram_help, new_yougile_event, \
                       additional_commands, state_proccessor, \
                       change_user_email, restart_session


# Логгер
log = logging.getLogger(__name__)

# Информация о пользователях. Например, почта, текущий этап и т.д.
users_info: dict[int, UserInfo] = {}


# Получение версии сервера
@app.get('/')
async def index():
    return {'version': '0.01'}


# Хука телеграмма
@app.post('/telegram')
async def telegram_webhook(update: TelegramUpdate):
    user = update.message.from_user
    cmd = update.message.text
    log.info(f'({user.username}) [{user.id}] запросил {cmd}')

 
    user_info: UserInfo = users_info.get(user.id)
    # Добавляет пользователя в список написавших, сохраняя этап и т.д.
    if user.id not in users_info:
        user_info: UserInfo = UserInfo(
            user_id=user.id,
            yougile_id=None,
            state=UserState.START
        )
        users_info[user.id] = user_info

    # Обработка команды
    match cmd:
        case '/start':
            await telegram_start(user)
        case '/help':
            await telegram_help(user)
        case '/change_email':
            user_info: UserInfo = await change_user_email(
                update.message.message_id,
                user_info
            )
        case '/stop':
            user_info: UserInfo = restart_session(user_info)
        case _:
            # Перенаправление незакреплённых команд
            user_info: UserInfo = await additional_commands(
                update.message,
                user_info
            )

    # Обработка состояний
    user_info: UserInfo = await state_proccessor(user, user_info)
    if user_info.is_changed:
        user_info.is_changed = False
        # "Применяем" изменения
        users_info[user.id] = user_info

    return {'version': '0.01'}


# Хук YouGile
@app.post('/yougile')
async def yougile_webhook(update: YouGileTaskUpdate):
    task = update.payload
    log.info('Получение задачи "%s" статус: %s', task.title, update.event)

    # Отправляем задачу
    await new_yougile_event(update.event, task)

    return {'version': '0.01'}
