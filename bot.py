import telebot
from telebot import types
from authorization import BOT_TOKEN
import main

cazi_bot = telebot.TeleBot(BOT_TOKEN) # get token for cazi_bot

@cazi_bot.message_handler(content_types=['text'])



def print_current_tasks(message): # this funct print current task from main.current_tasks
    if message.text == "Распечатай актуальные задачи":
        cazi_bot.send_message(message.from_user.id, f"<b>На данный момент актуальнными задачами являются</b>: \n\n{main.current_task(main.LIST_TASKS)}", parse_mode='HTML')
    else:
        cazi_bot.send_message(message.from_user.id, "Напечатай \"Распечатай актуальные задачи\"")




cazi_bot.polling(none_stop=True, interval=0) # method for waiting message from users
