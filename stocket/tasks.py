from celery import shared_task
from stocket.models import Portfolio
from stocket.views.utils import performance_snapshot_portfolio


@shared_task
def performance_snapshot():
    # the background task creates hourly snapshot for all active portfolios at XX:31:00
    # available hours: 09:30, 10:30, 11:30, 12:30, 13:30, 14:30, 15:30
    active_portfolios = Portfolio.objects.filter(is_active=True)
    for portfolio in active_portfolios.iterator():
        performance_snapshot_portfolio(portfolio)
