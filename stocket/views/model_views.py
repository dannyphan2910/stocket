from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from stocket.serializers import *
from .utils import *

# Create your views here.


class UserView(APIAuthRequest, ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class AccountView(APIAuthRequest, ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    @action(methods=['get'], detail=True, url_path='portfolios/current')
    def get_current_portfolio(self, request, *args, **kwargs):
        account = self.get_object()
        current_portfolio = get_current_portfolio(account)
        serializer = PortfolioSerializer(current_portfolio, many=False)

        response = serializer.data
        try:
            breakdown = get_portfolio_breakdown(current_portfolio)
        except KeyError as e:
            return handle_logic_errors('API error occurred')

        response['breakdown'] = breakdown

        return Response(response)

    @action(methods=['get'], detail=True, url_path='portfolios')
    def get_all_portfolio(self, request, *args, **kwargs):
        account = self.get_object()
        portfolios = account.portfolio_set.order_by('-created_at')
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)


class PortfolioView(APIAuthRequest, ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    filterset_fields = ('account')

    def create(self, request, *args, **kwargs):
        data = request.data
        account_id = int(data['account'])
        response = super(TransactionView, self).create(request, args, kwargs)

        if response.status_code == 200:
            account = Account.objects.get(pk=account_id)
            discard_old_portfolio(account)

        return response


class TransactionView(APIAuthRequest, ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filterset_fields = ('portfolio', 'transaction_type')

    def create(self, request, *args, **kwargs):
        data = request.data
        portfolio_id = int(data['portfolio'])

        try:
            account = get_account_by_portfolio(portfolio_id)
        except (Portfolio.DoesNotExist, Portfolio.MultipleObjectsReturned) as e:
            return handle_request_errors(str(e))

        if portfolio_id != get_current_portfolio(account).id:
            return handle_request_errors("transaction must be made for the account's current portfolio")

        amount = data['amount']
        order_price = data['order_price']
        price = round(amount * order_price, 2)
        transaction_type = int(data['transaction_type'])

        if transaction_type == 0 and account.balance < price:
            return handle_logic_errors("account balance insufficient")

        response = super(TransactionView, self).create(request, args, kwargs)

        if response.status_code == 200:
            update_balance(account, transaction_type, price)

        return response


class SnapshotView(APIAuthRequest, ModelViewSet):
    serializer_class = SnapshotSerializer
    queryset = Snapshot.objects.all()
    filterset_fields = ('portfolio',)

    def list(self, request, *args, **kwargs):
        portfolio_id = request.query_params.get('portfolio')
        all_snapshots = []
        if portfolio_id is None:
            active_portfolios = Portfolio.objects.filter(is_active=True).order_by('id')
            for portfolio in active_portfolios.iterator():
                all_snapshots.extend(performance_snapshot_portfolio(portfolio.id))
        else:
            all_snapshots.extend(performance_snapshot_portfolio(portfolio_id))
        serializer = SnapshotSerializer(all_snapshots, many=True)
        return Response(serializer.data)

















