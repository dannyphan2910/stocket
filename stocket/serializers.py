from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'user', 'balance', 'created_at')


class PortfolioSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'account', 'version', 'created_at', 'transactions')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'portfolio', 'transaction_type', 'ticker_symbol', 'amount', 'order_price', 'created_at')
