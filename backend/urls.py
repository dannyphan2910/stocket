"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from stocket.views import *


router = routers.DefaultRouter()
router.register(r'users', UserView, 'user')
router.register(r'accounts', AccountView, 'account')
router.register(r'portfolios', PortfolioView, 'portfolio')
router.register(r'transactions', TransactionView, 'transaction')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/', include('rest_framework.urls')),
    path('api/users/', include('django.contrib.auth.urls')),

    path('api/tickers/base', TickerBase.as_view()),
    path('api/tickers/base/modules', TickerModules.as_view()),
    path('api/tickers/financials', TickerFinancials.as_view()),
    path('api/tickers/financials/modules', TickerFinancialModules.as_view()),
    path('api/tickers/options', TickerOptions.as_view()),
    path('api/tickers/history', TickerHistoricalPrices.as_view()),
    path('api/tickers/events', TickerEvents.as_view()),
    path('api/tickers/insights', TickerInsights.as_view()),

    path('api/news', News.as_view()),
    path('api/screeners/modules', ScreenerModules.as_view()),
    path('api/screeners', Screener.as_view()),
    path('api/search', Search.as_view()),
]
