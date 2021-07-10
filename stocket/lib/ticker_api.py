from yahooquery import Ticker, Screener, search as yq_search
from datetime import datetime
from .utils import *


def get_tickers_base(ticker_symbols, modules=None):
    if ticker_symbols is None:
        raise ValueError('no ticker symbol requested')

    tickers = Ticker(symbols=ticker_symbols, asynchronous=True)

    if modules is not None:
        try:
            response = tickers.get_modules(modules=modules)
        except ValueError:
            raise ValueError(f'at least jone of modules requested is not a valid value: {modules}')

    else:
        response = tickers.all_modules

    return response


def get_tickers_financial(ticker_symbols, modules=None, frequency='a', trailing=True):
    if ticker_symbols is None:
        raise ValueError('no ticker symbol requested')

    if frequency not in ('a', 'c'):
        raise ValueError(f'invalid frequency: {frequency}')

    tickers = Ticker(symbols=ticker_symbols, asynchronous=True)

    if modules is not None:
        try:
            df = tickers.get_financial_data(types=modules, frequency=frequency, trailing=trailing)
            response = df_to_dict(df) if not isinstance(df, dict) else df
        except ValueError:
            raise ValueError(f'at least jone of modules requested is not a valid value: {modules}')

    else:
        df = tickers.all_financial_data(frequency=frequency)
        response = df_to_dict(df) if not isinstance(df, dict) else df

    return response


def get_tickers_historical(ticker_symbols, period='ytd', interval='1d', start=None, end=None, adj_timezone=True, adj_ohlc=False, df_by_date=False):
    if ticker_symbols is None:
        raise ValueError('no ticker symbol requested')

    if period not in ('1d', '5d', '7d', '60d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'):
        raise ValueError(f'invalid frequency: {period}')

    if interval not in ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'):
        raise ValueError(f'invalid interval: {interval}')

    if start is not None and not (isinstance(start, str) or isinstance(start, datetime)):
        raise ValueError(f'invalid start date (YYYY-MM-DD): {start}')

    if end is not None and not (isinstance(end, str) or isinstance(end, datetime)):
        raise ValueError(f'invalid end date (YYYY-MM-DD): {end}')

    tickers = Ticker(ticker_symbols, asynchronous=True)

    if start is not None and end is not None:
        df = tickers.history(
            period=period,
            interval=interval,
            start=start,
            end=end,
            adj_timezone=adj_timezone,
            adj_ohlc=adj_ohlc
        )
    elif start is not None:
        df = tickers.history(
            period=period,
            interval=interval,
            start=start,
            adj_timezone=adj_timezone,
            adj_ohlc=adj_ohlc
        )
    elif end is not None:
        df = tickers.history(
            period=period,
            interval=interval,
            end=end,
            adj_timezone=adj_timezone,
            adj_ohlc=adj_ohlc
        )
    else:
        df = tickers.history(
            period=period,
            interval=interval,
            adj_timezone=adj_timezone,
            adj_ohlc=adj_ohlc
        )

    if df_by_date:
        df = set_date_primary_key(df)

    index_name = 'date' if df_by_date else 'symbol'
    response = df_to_dict(df, index_name) if not isinstance(df, dict) else df

    return response


def get_tickers_option_chain(ticker_symbols, expiration=None, option_type=None):
    if ticker_symbols is None:
        raise ValueError('no ticker symbol requested')

    if expiration is not None and not (isinstance(expiration, str) or isinstance(expiration, datetime)):
        raise ValueError(f'invalid expiration date (YYYY-MM-DD): {expiration}')

    if option_type not in ('puts', 'calls'):
        raise ValueError(f'invalid option type ("puts", "calls"): {option_type}')

    tickers = Ticker(symbols=ticker_symbols, asynchronous=True)

    df = tickers.option_chain
    try:
        if expiration is not None and option_type is not None:
            df = df.loc[expiration, option_type]
        elif expiration is not None:
            df = df.loc[expiration]
        elif option_type is not None:
            df = df.loc[option_type]
    except KeyError:
        raise ValueError(f'the specified expiration and/or option type are not available: {expiration}, {option_type}')

    response = df_to_dict(df) if not isinstance(df, dict) else df
    return response


def get_tickers_events(ticker_symbols):
    if ticker_symbols is None:
        raise ValueError('no ticker symbol requested')

    tickers = Ticker(symbols=ticker_symbols, asynchronous=True)

    df_events = tickers.corporate_events

    if not isinstance(df_events, str):
        response = df_to_dict(df_events)
    else:
        raise ValueError(df_events)
    return response


def get_tickers_insights(ticker_symbols):
    if ticker_symbols is None:
        raise ValueError('no ticker symbol requested')

    tickers = Ticker(symbols=ticker_symbols, asynchronous=True)

    technical_insights = tickers.technical_insights
    recommendations = tickers.recommendations

    response = pair_symbol_json(technical_insights, 'technical_insights', recommendations, 'recommendations')
    return response


def get_news(ticker_symbols, count=10):
    if ticker_symbols is None:
        raise ValueError('no ticker symbol requested')

    count = int(count)
    if count <= 0:
        raise ValueError('invalid count')

    tickers = Ticker(symbols=ticker_symbols, asynchronous=True)

    response = tickers.news(count)
    return response


def get_all_screeners():
    return Screener().available_screeners


def get_screeners(screeners, count=10):
    if screeners is None or not isinstance(screeners, list) or len(screeners) == 0:
        raise ValueError('no screeners requested')

    count = int(count)
    if count <= 0:
        raise ValueError('invalid count')

    response = Screener().get_screeners(screeners, count)
    return response


def search(query, count=10):
    if query is None or not isinstance(query, str):
        raise ValueError('no query requested')

    count = int(count)
    if count <= 0:
        raise ValueError('invalid count')

    response = yq_search(query, quotes_count=count, news_count=count)
    return response




