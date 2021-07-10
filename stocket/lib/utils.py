import json
import decimal
import pandas as pd
from .ticker_api import *


def df_to_dict(df, primary_index_name='symbol'):
    df.reset_index(inplace=True)
    df.set_index(primary_index_name, inplace=True)
    result = {}
    for _, row in df.iterrows():
        key = row.name
        if isinstance(key, pd.Timestamp):
            key = key.to_pydatetime()
        result.setdefault(key, [])
        data = row.to_json()  # auto-convert nan to null
        result[key].append(json.loads(data))

    return result


def set_date_primary_key(df):
    return df.reset_index().set_index('date').sort_values('date')


def pair_symbol_json(dict1, name1, dict2, name2):
    result = {}
    for symbol, data in dict1.items():
        result.setdefault(symbol, {})
        result[symbol][name1] = data

    for symbol, data in dict2.items():
        result.setdefault(symbol, {})
        result[symbol][name2] = data

    return result


def get_market_value(ticker_symbol, total_shares):
    ticker_info = get_tickers_base(ticker_symbol, 'price')[ticker_symbol]
    market_state = ticker_info['marketState']
    if market_state == 'REGULAR':
        market_price = ticker_info['regularMarketPrice']
    elif market_state == 'PRE':
        market_price = ticker_info['preMarketPrice']
    else:  # == 'POST'
        market_price = ticker_info['postMarketPrice']
    market_value = round(total_shares * decimal.Decimal(market_price), 2)
    return market_value

