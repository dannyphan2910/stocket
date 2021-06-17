import decimal
from datetime import datetime, timedelta
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


def discard_old_portfolio(account):
    portfolios = account.portfolio_set.order_by('-created_at')
    if len(portfolios) > 1:
        old_portfolios = portfolios[1:]
        old_portfolios.update(is_active=False)


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


def performance_snapshot_portfolio(portfolio_id):
    all_snapshots = []
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    transactions = Transaction.objects.filter(portfolio=portfolio)
    if transactions.exists():
        time_record = datetime.now().replace(microsecond=0, second=0, minute=30)
        is_current_market = datetime.now().replace(microsecond=0, second=0, minute=30, hour=9) \
                            <= time_record \
                            <= datetime.now().replace(microsecond=0, second=0, minute=59, hour=15)
        snapshots = Snapshot.objects.filter(portfolio=portfolio)
        # only get the snapshot for opening hours
        if not is_current_market:
            # if not snapshot created or if the latest snapshot is not created for the last hour
            # we populate the table using historical hourly pricing for the year (if no snapshot)
            # or for the hours after the last snapshot
            # else, create the snapshot for the most recent opening hour (XX:30:00)
            if not snapshots.exists():
                start_date = portfolio.created_at
            elif not last_record_is_latest(snapshots.order_by('-time_record').first().time_record):
                start_date = snapshots.order_by('-time_record').first().time_record
            else:
                start_date = time_record
            print(start_date)

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ticker_symbol, SUM(amount * (IF(transaction_type = 1, -1, 1))) as total_shares "
                    "FROM stocket_transaction "
                    "WHERE portfolio_id = %s "
                    "GROUP BY ticker_symbol;", (portfolio.id,))

                portfolio_dict = {}
                for ticker_symbol, total_shares in cursor.fetchall():
                    portfolio_dict[ticker_symbol] = total_shares

                history = get_tickers_historical(
                    ticker_symbols=portfolio_dict.keys(),
                    interval='1h',
                    start=start_date,
                    df_by_date=True
                )
                # loop until now
                for time, record in history.items():
                    total_value = 0
                    if time <= time_record:
                        for entry in record:
                            total_value += decimal.Decimal(entry['close']) * portfolio_dict[entry['symbol']]

                        new_snapshot = Snapshot(portfolio=portfolio,
                                                market_value=round(total_value, 2),
                                                time_record=time)
                        all_snapshots.append(new_snapshot)
    return all_snapshots


def last_record_is_latest(last_time_record):
    last_time_record = datetime(last_time_record)
    base_last_record = last_time_record.replace(microsecond=0, second=0, minute=0, hour=0)
    now = datetime.now().replace(microsecond=0, second=0, minute=30) # guaranteed to be in current market hours
    base_now = now.replace(microsecond=0, second=0, minute=0, hour=0)

    if base_now == base_last_record + timedelta(days=1) and (now.hour == 9 and last_time_record.hour == 15) \
            and (now.minute == last_time_record.minute):
        return True
    if base_now == base_last_record and now == last_time_record + timedelta(hours=1):
        return True
    return False


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
