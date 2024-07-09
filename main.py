import telebot
import config
from telebot import types
import get_transactions
from flask import Flask, request
import handlers

secret = '####'
url = '####' + secret

bot = telebot.TeleBot(config.Token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=url)


app = Flask(__name__)
handlers.check_address_handlers(bot)


@app.route('/webhook_update' + secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200



# Обработчик команды /start в приватном чате
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    # Проверяем, что сообщение пришло из приватного чата
    if message.chat.type == 'private':

        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEMRYJmZRKPofwgX63RElacVAk8zy-gegAC0wADVp29CvUyj5fVEvk9NQQ")
        bot.send_message(message.chat.id, "Привет! Я готов приступить к работе 😊")
        bot.send_message(message.chat.id, "Наш канал: @getscanton 📰")

        # Создаем клавиатуру
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton('Проверить адрес')
        btn2 = types.KeyboardButton('Информация')
        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

    else:
        pass


@bot.message_handler(func=lambda message: message.text == 'Информация')
def information(message):
    bot.send_message(message.chat.id, "Вы всегда можете обратиться ко мне, если бот работает некорректно, у вас есть предложения или вопросы. Я рад любым отзывам и всегда готов помочь!\n\nПодпишитесь на наш канал: @\nРазработчик: @\n\n💎 Поддержка бота:\n\nUQBHindLjVUAdBCLmkNSk0kwr8XYwX0nOFFuYxBzQ-LFkh9u")


@bot.callback_query_handler(func=lambda call: call.data.startswith('transactions_'))
def handle_transaction_callback(call):
    # Используем partition вместо split, чтобы избежать проблем с подчеркиваниями в адресе
    prefix, separator, address = call.data.partition('_')

    transactions = get_transactions.get_transaction_account(address)

    if transactions:
        for result_transaction in transactions:
            message_text = (f"💎 Сумма транзакции: {result_transaction['value']} TON\n"
                            f"🔀 Направление: {result_transaction['direction']}")
            if 'comment' in result_transaction and result_transaction['comment']:
                message_text += f"\n✉️ Комментарий: {result_transaction['comment']}"
            bot.send_message(call.message.chat.id, message_text)
    else:
        bot.send_message(call.message.chat.id, "Не удалось получить данные о транзакциях. Или их нет 😞")
