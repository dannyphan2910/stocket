from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TRANSACTION_TYPES = [
    (0, 'BUY'),
    (1, 'SELL')
]


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # max = 9 999 999 999 . 99
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (balance: {self.balance})"


class Portfolio(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # the only active version will the be latest one

    def __str__(self):
        return f"user #{self.account_id}: {self.title}"

    class Meta:
        unique_together = ['account_id', 'title']


class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPES)
    ticker_symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=11, decimal_places=5)  # max = 999 999 . 99999
    order_price = models.DecimalField(max_digits=8, decimal_places=2)  # max = 999 999 . 99
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"portfolio #{self.portfolio_id}: {'BUY' if self.transaction_type == 0 else 'SELL'} {self.amount} " \
               f"of {self.ticker_symbol} at {self.order_price} per share"

    @property
    def total_change(self):
        price = round(self.amount * self.order_price, 2)
        return price if self.transaction_type == 1 else -price  # sell -> +amount*price; buy -> -amount*price

    class Meta:
        order_with_respect_to = 'portfolio'
