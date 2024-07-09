from telebot import types
import func
import config


def check_address_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == 'Проверить адрес')
    def check_address(message):
        # Создаем клавиатуру с кнопкой "Отменить"
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        cancel_button = types.KeyboardButton('Отменить')
        markup.add(cancel_button)

        bot.send_message(message.chat.id, "Пожалуйста, отправьте мне TON адрес для проверки или нажмите 'Отменить':", reply_markup=markup)
        bot.register_next_step_handler(message, handle_address)

    def handle_address(message):
        if message.text == 'Отменить':
            # Создаем клавиатуру для главного меню
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn1 = types.KeyboardButton('Проверить адрес')
            btn2 = types.KeyboardButton('Информация')
            markup.add(btn1, btn2)

            bot.send_message(message.chat.id, "Действие отменено. Возвращаю в главное меню.", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "📡 Провожу сканирование...")
            address = message.text.strip()
            get_address = func.get_address_info(address)

            # Создаем клавиатуру для главного меню
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn1 = types.KeyboardButton('Проверить адрес')
            btn2 = types.KeyboardButton('Информация')
            markup.add(btn1, btn2)

            if get_address:
                if get_address['status'] == "active":
                    account_status = "Активный ✅"
                else:
                    account_status = "Неактивный 😔"

                if get_address['is_scam'] is None:
                    account_status_scam = "Аккаунт не был замечен в мошеничестве 👍"
                else:
                    account_status_scam = "Будьте осторожны! Аккаунт помечен как мошенический 🤬"

                bot.send_message(
                    message.chat.id,
                    f"Адрес: <a href='https://tonscan.org/ru/address/{address}'>{address}</a>",
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )

                bot.send_message(message.chat.id,
                                 f"Баланс в TON: {get_address['balance_ton']}💎 ${get_address['balance_usd']}\n\n"
                                 f"Статус аккаунта: {account_status}\n"
                                 f"Последняя активность: {get_address['account_last_activity']}\n\n"
                                 f"Аккаунт метка: {account_status_scam}", reply_markup=markup)

                bot.send_message(message.chat.id, "Ссылка на чек: <a href='https://t.me/xrocket?start=mc_5rYUP5LEJcTU4N8'>ТЫК =)</a>", parse_mode="HTML", disable_web_page_preview=True)


                # Создаем инлайн-кнопку для показа транзакций
                inline_markup = types.InlineKeyboardMarkup()
                inline_btn = types.InlineKeyboardButton(text="Показать последние 10 транзакций",
                                                        callback_data=f"transactions_{address}")
                inline_markup.add(inline_btn)
                bot.send_message(message.chat.id, "Вы можете посмотреть последние 10 транзакций по этому адресу:",
                                 reply_markup=inline_markup)


                # Отправляем отчет в канал
                bot.send_message(config.CHANNEL_ID,
                                 f"Пользователь @{message.from_user.username} проверил адрес:\n"
                                 f"Адрес: <a href='https://tonscan.org/ru/address/{address}'>{address}</a>\n"
                                 f"Баланс в TON: {get_address['balance_ton']}💎 ${get_address['balance_usd']}\n\n"
                                 f"Статус аккаунта: {account_status}\n"
                                 f"Последняя активность: {get_address['account_last_activity']}\n\n"
                                 f"Аккаунт метка: {account_status_scam}",
                                 parse_mode="HTML",
                                 disable_web_page_preview=True)


            else:
                bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEMRYRmZRU7CJCMoBzmrmqNmSnMZLXvfwAC5AADVp29Chab7Y_u8TUENQQ")
                bot.send_message(message.chat.id,
                                 "Не удалось получить данные. Проверьте правильность ввода или обратитесь к разработчику для устранения проблемы.")
                bot.send_message(message.chat.id,
                                 "Написать: t.me/superset69",
                                 reply_markup=markup)
