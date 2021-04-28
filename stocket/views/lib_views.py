from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from stocket.lib import *
from .utils import *


class TickerBase(APIView):
    def get(self, request):
        data = request.query_params
        ticker_symbols = data['tickers'] if 'tickers' in data.keys() else None
        modules = data['modules'] if 'modules' in data.keys() else None

        try:
            response = get_tickers_base(ticker_symbols, modules)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class TickerModules(APIView):
    def get(self, request):
        return Response(Ticker.MODULES)


class TickerFinancials(APIView):
    def get(self, request):
        data = request.query_params
        ticker_symbols = data['tickers'] if 'tickers' in data.keys() else None
        modules = data['modules'] if 'modules' in data.keys() else None
        frequency = data['frequency'] if 'frequency' in data.keys() else 'a'
        trailing = data['trailing'] if 'trailing' in data.keys() else True

        try:
            response = get_tickers_financial(ticker_symbols, modules, frequency, trailing)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class TickerFinancialModules(APIView):
    def get(self, request):
        return Response(Ticker.FUNDAMENTALS_OPTIONS)


class TickerOptions(APIView):
    def get(self, request):
        data = request.query_params
        ticker_symbols = data['tickers'] if 'tickers' in data.keys() else None
        expiration = data['expiration'] if 'tickers' in data.keys() else None
        option_type = data['type'] if 'tickers' in data.keys() else None

        try:
            response = get_tickers_option_chain(ticker_symbols, expiration, option_type)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class TickerHistoricalPrices(APIView):
    def get(self, request):
        data = request.query_params
        ticker_symbols = data['tickers'] if 'tickers' in data.keys() else None
        period = data['period'] if 'period' in data.keys() else 'ytd'
        interval = data['interval'] if 'interval' in data.keys() else '1d'
        start = data['start'] if 'start' in data.keys() else None  # YYYY-MM-DD
        end = data['end'] if 'end' in data.keys() else None  # YYYY-MM-DD
        adj_timezone = data['adj_timezone'] if 'adj_timezone' in data.keys() else True
        adj_ohlc = data['adj_ohlc'] if 'adj_ohlc' in data.keys() else False

        try:
            response = get_tickers_historical(ticker_symbols, period, interval, start, end, adj_timezone, adj_ohlc)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class TickerEvents(APIView):
    def get(self, request):
        data = request.query_params
        ticker_symbols = data['tickers'] if 'tickers' in data.keys() else None

        try:
            response = get_tickers_events(ticker_symbols)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class TickerInsights(APIView):
    def get(self, request):
        data = request.query_params
        ticker_symbols = data['tickers'] if 'tickers' in data.keys() else None

        try:
            response = get_tickers_insights(ticker_symbols)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class News(APIView):
    def get(self, request):
        data = request.query_params
        ticker_symbols = data['tickers'] if 'tickers' in data.keys() else None
        count = data['count'] if 'count' in data.keys() else 10

        try:
            response = get_news(ticker_symbols, count)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class ScreenerModules(APIView):
    def get(self, request):
        return Response(get_all_screeners())


class Screener(APIView):
    def get(self, request):
        data = request.query_params
        screeners = data['screeners'] if 'screeners' in data.keys() else None
        count = data['count'] if 'count' in data.keys() else 10

        try:
            response = get_screeners(screeners, count)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


class Search(APIView):
    def get(self, request):
        data = request.query_params
        query = data['query'] if 'query' in data.keys() else None
        count = data['count'] if 'count' in data.keys() else 10

        try:
            response = search(query, count)
        except ValueError as e:
            return handle_request_errors(str(e))

        return Response(response)


