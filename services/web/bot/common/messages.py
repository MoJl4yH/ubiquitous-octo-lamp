"""
    Файл с обработкой текста сообщений бота.
"""

import os
import json

from string import Template
from datetime import datetime

from .models import YouGileTask
from .validators import remove_html


# Константы
MESSAGES_FILE_PATH = os.environ['MESSAGES_PATH']
RESERVED_CHARACTERS = ('!', '.', '(', ')', '-')
YOUGILE_EVENTS: dict = {
    'created': 'создана',
    'deleted': 'удалена',
    'restored': ' восстановлена',
    'moved': 'перемещена',
    'renamed': 'переименована',
    'updated': 'обновлена',
}

def replace_reserved_chars(text: str, mode: str = None) -> str:
    """ Экранирует все зарезервированные маркдауном символы. """
    if not text:
        return ''

    chars = RESERVED_CHARACTERS
    if mode == 'all':
        chars = RESERVED_CHARACTERS + ('*', '_', '~', '|', '[', ']', '`')

    # TODO: под собранную регулярку
    for char in chars:
        text = text.replace(char, f'\\{char}')
    return text


# Переписываем safe_substitute
old_safe_substitute = Template.safe_substitute
def expand_safe_substitute(self, **kwargs):
    for key, value in kwargs.items():
        kwargs[key] = replace_reserved_chars(value, mode='all')
    return old_safe_substitute(self, **kwargs)
Template.safe_substitute = expand_safe_substitute


# Читаем файл и получает словарь сообщений
with open(MESSAGES_FILE_PATH, 'r') as messages_file:
    raw_messages: dict = json.load(messages_file)

# Преобразуем словарь, используя string Template
DEFAULT_MESSAGES: dict[str, Template] = {}
for message_name, message_text in raw_messages.items():
    # Для ТГ необходимо заменить зарезервированные маркдауном символы
    # e.g. ! -> \\!, . -> \\.
    message_text = replace_reserved_chars(message_text)

    DEFAULT_MESSAGES[message_name] = Template(message_text)


def yougile_task_to_text(task: YouGileTask, event: str = '') -> str:
    """ Преобразует задачу в текст, готовый к выводу. """
    deadline = 'не установлен'
    if task.deadline:
        deadline = datetime.fromtimestamp(task.deadline.deadline / 1000)
    description = 'пусто'
    if task.description:
        description = remove_html(task.description)

    return DEFAULT_MESSAGES['yougile_task'].safe_substitute(
        event=YOUGILE_EVENTS.get(event, '').capitalize(),
        title=task.title,
        deadline=str(deadline),
        description=description
    )
