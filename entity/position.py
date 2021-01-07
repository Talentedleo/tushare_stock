from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config

fields = config.get_value('DAILY_FIELDS')


class Position:
    """
    持有的股票详情
    """

    def __init__(self, stock_code, stock_num, stock_price=None):
        # 股票代码 stock code
        self._stock_code = stock_code
        # 股票数量 stock num
        self._stock_num = stock_num
        # 股票价格 stock price
        if stock_price is None:
            # 如果不传价格, 查询最近一天的收盘价格
            cli = Client(self._stock_code, 7, fields)
            # 因为拿到的数据是倒序的
            self._stock_price = cli.get_stock_df_daily()['close'].head(1).values[0]
        else:
            self._stock_price = stock_price

    @property
    def stock_code(self):
        return self._stock_code

    @stock_code.setter
    def stock_code(self, value):
        self._stock_code = value

    @property
    def stock_num(self):
        return self._stock_num

    @stock_num.setter
    def stock_num(self, value):
        if not isinstance(value, int):
            raise ValueError('num must be an integer!')
        if value % 100 > 0:
            raise ValueError('num must be the multiples of 100!')
        self._stock_num = value

    @property
    def stock_price(self):
        return self._stock_price

    @stock_price.setter
    def stock_price(self, value):
        if value < 0:
            raise ValueError('price must > 0 !')
        self._stock_price = value

    def __str__(self):
        return 'stock code: {}, cost price: {}, num: {}'.format(self._stock_code, self._stock_price, self._stock_num)


if __name__ == '__main__':
    # 京东方A '000725.SZ'
    # stock = Position('000725.SZ', 100, 5.5)
    left = 123 % 100
    print(left)
