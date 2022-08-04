import telebot
import config
import random

from telebot import types


cats = ['коты - экстрасенсы', 'кошка может родить 100-150 котят', 'самый большой кот весил 21,3 кг',
        'кошка может бежать со скоростью 48 км/ч', 'самый маленький кот весит 800 гр',
        'коту-боту не нужна еда (хотя и просит постоянно)', 'не все коты вызывают аллергию, и это не всегда зависит от пушистости']
sharks = ['Акулы старше деревьев', 'Мегалодоны были самыми крупными акулами, которые когда-либо жили', 'Некоторые акулы светятся в темноте',
          'Акулы практически не различают цвет', 'У акул есть свои личности', 'У акул есть свои личности', 'Акулы постоянно теряют и заменяют зубы',
          'По всему миру существует более 400 видов']

answers = ['Да просто супер!', 'Отлично!', 'Не очень, корм сильно подорожал!', 'В целом норм, но я устал на работе.', 'В норме!',
           'Бесят кожаные', 'Переведи на мой счет 5 кг корма премиум']


animations = ['static/cats/AnimatedSticker1.tgs', 'static/cats/AnimatedSticker2.tgs', 'static/cats/AnimatedSticker3.tgs', 'static/cats/AnimatedSticker4.tgs',
              'static/cats/AnimatedSticker5.tgs', 'static/cats/AnimatedSticker6.tgs', 'static/cats/AnimatedSticker7.tgs', 'static/cats/AnimatedSticker8.tgs']

animations_shark = ['static/sharks/AnimatedSticker_s1.tgs', 'static/sharks/AnimatedSticker_s2.tgs', 'static/sharks/AnimatedSticker_s3.tgs', 'static/sharks/AnimatedSticker_s4.tgs']


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("😺Факт о котиках")
    item2 = types.KeyboardButton("🦈Факт об акулах")
    item3 = types.KeyboardButton("😀Как дела?")

    markup.add(item1, item2, item3)


    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот созданный, чтобы быть подопытным котиком.\n"
                                      "Я знаю много важных фактов о котах.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '😺Факт о котиках':
            bot.send_message(message.chat.id, str(random.choice(cats)))
            sti = open((random.choice(animations)), 'rb')
            bot.send_sticker(message.chat.id, sti)
        elif message.text == '🦈Факт об акулах':
            bot.send_message(message.chat.id, str(random.choice(sharks)))
            sti = open((random.choice(animations_shark)), 'rb')
            bot.send_sticker(message.chat.id, sti)
        elif message.text == '😀Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, str(random.choice(answers) + ' А сам как?'), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ты сказал "' + message.text + '" А я не знаю, что сказть 😿. Чтобы узнать новый факт про кота нажми /start, и мы начнем все сначала')

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
            # bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text="Это тестовое уведомление")

    except Exception as e:
        print(repr(e))
# RUN
bot.polling(none_stop=True)
