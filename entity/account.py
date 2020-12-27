class Account:

    def __init__(self, account_name, balance=None, market_value=None, positions=None):
        # 账号名称 account name
        self._account_name = account_name
        # 账号余额 balance
        self._balance = balance
        # 账号总市值 total market value
        self._market_value = market_value
        # 账号头寸 position
        self._positions = positions

    @property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, value):
        self._account_name = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError('price must > 0 !')
        self._balance = value

    @property
    def market_value(self):
        return self._market_value

    @market_value.setter
    def market_value(self, value):
        if value < 0:
            raise ValueError('price must > 0 !')
        self._market_value = value

    @property
    def positions(self):
        return self._positions

    @positions.setter
    def positions(self, value):
        if len(value) == 0:
            raise ValueError('list is empty !')
        self._positions = value


if __name__ == '__main__':
    account = Account('aaaa')
    account.positions = []
