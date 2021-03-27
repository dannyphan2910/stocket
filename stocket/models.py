from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # max = 9 999 999 999 . 99
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}: balance {self.balance}"


class Portfolio(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    version = models.IntegerField()  # the only active version will the be latest one
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user #{self.account_id}: portfolio ver {self.version}"

    class Meta:
        unique_together = ['account_id', 'version']


class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    transaction_type = models.IntegerChoices('TransactionType', 'BUY SELL', start=0)
    ticker_symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=11, decimal_places=5)  # max = 999 999 . 99999
    order_price = models.DecimalField(max_digits=8, decimal_places=2)  # max = 999 999 . 99
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"portfolio #{self.portfolio_id}: {self.transaction_type} {self.amount} of {self.ticker_symbol} at " \
               f"{self.order_price} per share"

    def total_change(self):
        price = round(self.amount * self.order_price, 2)
        return price if self.transaction_type == 'SELL' else -price  # sell -> +amount*price; buy -> -amount*price

    class Meta:
        order_with_respect_to = 'portfolio'
