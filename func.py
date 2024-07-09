"""Parse address and display in all formats."""
from pytonapi import Tonapi
import config
from pycoingecko import CoinGeckoAPI
import datetime


cg = CoinGeckoAPI()


def get_address_info(address):
    try:
        # Инициализация TON API
        tonapi = Tonapi(api_key=config.API_KEY_TON)
        account = tonapi.accounts.get_info(account_id=address)

        # Получение текущей цены TON в USD с CoinGecko
        get_ton_price_json = cg.get_price(ids='the-open-network', vs_currencies='usd')
        ton_price = get_ton_price_json['the-open-network']['usd']

        # Получение баланса аккаунта в TON
        account_balance_ton = account.balance.to_amount()

        # Вычисление стоимости баланса в USD
        account_balance_usd = account_balance_ton * ton_price

        # Форматирование баланса
        formatted_balance_ton = f"{account_balance_ton:.3f}"
        formatted_balance_usd = f"{account_balance_usd:.2f}"

        # Получение дополнительных данных аккаунта
        account_status = account.status
        account_status_scam = account.is_scam
        account_address = account.address
        # Получаем метку времени от last_activity
        account_last_activity = account.last_activity

        # Преобразуем метку времени в объект datetime
        last_activity_datetime = datetime.datetime.fromtimestamp(account_last_activity)
        # Добавляем 3 часа
        last_activity_datetime_plus_3 = last_activity_datetime + datetime.timedelta(hours=3)

        # Формирование результата
        result = {
            'address': account_address,
            'balance_ton': formatted_balance_ton,
            'balance_usd': formatted_balance_usd,
            'status': account_status,
            'is_scam': account_status_scam,
            'account_last_activity': last_activity_datetime_plus_3
        }

        return result

    except Exception as e:
        print("Ошибка при запросе к TON API SDK:", e)
        return None
