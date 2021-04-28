import decimal

from django.http import JsonResponse
from django.db import connection
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from stocket.models import *
from stocket.lib import *


authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
permission_classes = [IsAuthenticated]

BREAKDOWN_DEFAULT = {
    'allocation': 0.0,
    'market_value': 0.0
}


class APIAuthRequest:
    authentication_classes = authentication_classes
    permission_classes = permission_classes


def get_account_by_portfolio(portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    return portfolio.account


def get_current_portfolio(account):
    return account.portfolio_set.order_by('-created_at').first()


def get_portfolio_breakdown(portfolio):
    transactions = portfolio.transaction_set
    total_investment = get_total_investments(transactions)

    # stock -> { allocation (in percentage), market_value }
    breakdown = {
        'total_investment': total_investment,
    }
    total_market_value = 0
    # check if any records exists
    if transactions.exists() and total_investment > 0:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ticker_symbol, SUM(amount * (IF(transaction_type = 1, -1, 1))) as total_shares, "
                           "SUM(order_price * amount * (IF(transaction_type = 1, -1, 1))) AS initial_investment "
                           "FROM stocket_transaction "
                           "GROUP BY ticker_symbol;")

            for ticker_symbol, total_shares, initial_investment in cursor.fetchall():
                allocation = round(initial_investment / total_investment, 2)
                market_value = get_market_value(ticker_symbol, total_shares)
                return_value = market_value - initial_investment
                total_market_value += market_value

                breakdown[ticker_symbol] = {
                    'investment': initial_investment,
                    'shares': total_shares,
                    'allocation': allocation,
                    'market_value': market_value,
                    'return': {
                        'is_positive': return_value > 0,
                        'value': return_value,
                        'percentage': round((market_value / initial_investment - 1) * 100, 2)
                    },
                }
            total_return_value = total_market_value - total_investment
            breakdown['total_return'] = {
                'is_positive': total_return_value > 0,
                'value': total_return_value,
                'percentage': round((total_market_value / total_investment - 1) * 100, 2)
            }

    return breakdown


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


def get_total_investments(transactions):
    total = 0
    if transactions.exists():
        with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(order_price * amount * (if (transaction_type = 1, -1, 1))) AS total_investment "
                           "FROM stocket_transaction")
            total = cursor.fetchone()[0]
    return total


def update_balance(account, transaction_type, price):
    # a BUY transaction decreases account balance
    if transaction_type == 0:
        account.balance -= price
    # a SELL transaction increases account balance
    elif transaction_type == 1:
        account.balance += price
    account.save()


def handle_request_errors(message):
    data = {
        'error_status': 400,
        'message': message
    }
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def handle_logic_errors(message):
    data = {
        'error_status': 500,
        'message': message
    }
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
