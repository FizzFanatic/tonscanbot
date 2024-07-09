"""Get account transactions."""
from pytonapi import Tonapi
from pytonapi.utils import nano_to_amount
import config


def format_value(value, precision=9):
    # Форматируем значение с фиксированным числом десятичных знаков, убираем лишние нули
    formatted_value = f"{value:.{precision}f}".rstrip('0').rstrip('.')
    return formatted_value


def get_transaction_account(address):
    try:
        print(f"Полученный адрес: {address}")
        tonapi = Tonapi(api_key=config.API_KEY_TON)
        result = tonapi.blockchain.get_account_transactions(account_id=address, limit=10)

        transactions_list = []

        for transaction in result.transactions:
            # Обрабатываем входящие сообщения
            if transaction.in_msg and transaction.in_msg.value > 0:
                value = nano_to_amount(transaction.in_msg.value, precision=9)
                formatted_value = format_value(value)
                transaction_info = {
                    "direction": "Входящая 💚",
                    "value": formatted_value,
                    "comment": transaction.in_msg.decoded_body['text'] if transaction.in_msg.decoded_op_name == "text_comment" else None
                }
                transactions_list.append(transaction_info)

            # Обрабатываем исходящие сообщения
            for out_msg in transaction.out_msgs:
                if out_msg.value > 0:
                    value = nano_to_amount(out_msg.value, precision=9)
                    formatted_value = format_value(value)
                    transaction_info = {
                        "direction": "Исходящая ❤️",
                        "value": formatted_value,
                        "comment": out_msg.decoded_body['text'] if out_msg.decoded_op_name == "text_comment" else None
                    }
                    transactions_list.append(transaction_info)

        return transactions_list

    except Exception as e:
        print("Ошибка при запросе к TON API SDK:", e)
        return None
