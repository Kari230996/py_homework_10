'''
Прикрутить бота к задачам с предыдущего семинара:
Создать калькулятор для работы с рациональными и комплексными числами, организовать меню,
добавив в неё систему логирования
'''


import telebot
from telebot import types
import random
import logging

bot = telebot.TeleBot("5911932496:AAHGeapoQveYTYXt2Z4SH6_0Lf8ymexERJ8")

sweets = 221
max_sweet = 28

flag = None

# Для калькулятора
# -------------------------------------------------------
value = ''
old_value = ''




keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(    telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                 telebot.types.InlineKeyboardButton('C', callback_data='C'),
                 telebot.types.InlineKeyboardButton('<=', callback_data='<='),
                 telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(    telebot.types.InlineKeyboardButton('7', callback_data='7'),
                 telebot.types.InlineKeyboardButton('8', callback_data='8'),
                 telebot.types.InlineKeyboardButton('9', callback_data='9'),
                 telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(    telebot.types.InlineKeyboardButton('4', callback_data='4'),
                 telebot.types.InlineKeyboardButton('5', callback_data='5'),
                 telebot.types.InlineKeyboardButton('6', callback_data='6'),
                 telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(    telebot.types.InlineKeyboardButton('1', callback_data='1'),
                 telebot.types.InlineKeyboardButton('2', callback_data='2'),
                 telebot.types.InlineKeyboardButton('3', callback_data='3'),
                 telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(    telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                 telebot.types.InlineKeyboardButton('0', callback_data='0'),
                 telebot.types.InlineKeyboardButton('.', callback_data='.'),
                 telebot.types.InlineKeyboardButton('=', callback_data='='))


@bot.message_handler(commands = ['calculator'])
def get_message(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)

    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value) - 1]
    elif data == '=':
        try:
            value = str( eval(value) )
        except:
            value = 'Error!'
    else:
        value += data

    if (value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0',
                                  reply_markup=keyboard)
            old_value = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value,
                                  reply_markup=keyboard)
            old_value = value

        if value == 'Error!': value = ''




#bot.polling(none_stop=False, interval=0)



# --------------------------------------------------------------
# Для игры с конфетами
# --------------------------------------------------------------
@bot.message_handler(commands = ['start'])  # вызов функции по команде в списке
def start(message):
    global flag
    bot.send_message(message.chat.id, f"Welcome to my game!")
    flag = random.choice(['user', 'bot'])
    bot.send_message(message.chat.id, f'Overall, there are {sweets} sweets')
    if flag == 'user':
        bot.send_message(message.chat.id, "It's your first turn")
    else:
        bot.send_message(message.chat.id, "First turn for bot")

    controller(message)


def controller(message):
    global flag
    if sweets > 0:
        if flag == 'user':
            bot.send_message(message.chat.id, f"Your turn. Choose a number from 0 to {max_sweet}")
            bot.register_next_step_handler(message, user_input)
        else:
            bot_input(message)

    else:
        flag = 'user' if flag == 'bot' else 'bot'
        bot.send_message(message.chat.id, f'The winner is {flag}')

def bot_input(message):
    global flag, sweets
    if sweets <= max_sweet:
        bot_turn = sweets
    elif sweets % max_sweet == 0:
        bot_turn = max_sweet - 1
    else:
        bot_turn = sweets % max_sweet - 1
    sweets -= bot_turn
    bot.send_message(message.chat.id, f'The bot took {bot_turn} sweets')
    bot.send_message(message.chat.id, f'There are {sweets} sweets left')
    flag = 'user' if flag == 'bot' else 'bot'

    controller(message)

def user_input(message):
    global sweets, flag
    user_turn = int(message.text)
    if user_turn > 28 or user_turn < 0:
        bot.send_message(message.chat.id, 'You have choose a wrong number!')

    else:
        sweets -= user_turn
        bot.send_message(message.chat.id, f'There are {sweets} sweets left')
        flag = 'user' if flag == 'bot' else 'bot'

    controller(message)
# -----------------------------------------------------------------------



bot.infinity_polling()

