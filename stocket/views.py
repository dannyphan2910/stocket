from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import *
from .models import *

# Create your views here.

authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
permission_classes = [IsAuthenticated]


class APIAuthView:
    authentication_classes = authentication_classes
    permission_classes = permission_classes


class UserView(APIAuthView, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class AccountView(APIAuthView, viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class PortfolioView(APIAuthView, viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()


class TransactionView(APIAuthView, viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()






