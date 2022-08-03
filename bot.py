import telebot
import config
import random

from telebot import types


cats = ['коты - экстрасенсы', 'кошка может родить 100-150 котят', 'самый большой кот весил 21,3 кг',
        'кошка может бежать со скоростью 48 км/ч', 'самый маленький кот весит 800 гр',
        'коту-боту не нужна еда (хотя и просит постоянно)']
answers = ['Да просто супер!', 'Отлично!', 'Не очень, корм сильно подорожал!', 'В целом норм, но я устал на работе.', 'В норме!']


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("😺Факт о котиках")
    item2 = types.KeyboardButton("😀Как дела?")

    markup.add(item1, item2)


    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот созданный, чтобы быть подопытным котиком.\n"
                                      "Я знаю много важных фактов о котах.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '😺Факт о котиках':
            bot.send_message(message.chat.id, str(random.choice(cats)))
        elif message.text == '😀Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, str(random.choice(answers) + ' А сам как?'), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ты сказал "' + message.text + '" А я не знаю, что сказть 😿. Чтобы узнать новый факт про кота напиши /start')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько😺')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Не грусти давай😿')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😀Как дела?",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text="Это тестовое уведомление")

    except Exception as e:
        print(repr(e))
# RUN
bot.polling(none_stop=True)
