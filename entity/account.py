class Account:

    def __init__(self, account_name, balance=0, positions=None):
        # 账号名称 account name
        self._account_name = account_name
        # 账号余额 balance
        self._balance = balance
        # 账号头寸 position
        if positions is None:
            positions = []
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
    def positions(self):
        return self._positions

    @positions.setter
    def positions(self, value):
        self._positions = value

    def __str__(self):
        show_str = ''
        for po in self.positions:
            show_str = show_str + po.stock_code + ' price: ' + str(po.stock_price) + ' num: ' + str(po.stock_num) + '; '
        return 'account name: {}, balance: {}, positions: {}'.format(self.account_name, self.balance, show_str)


if __name__ == '__main__':
    account = Account('aaaa')
    account.positions = []
