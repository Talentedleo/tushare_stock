# 只是用来打印用的
from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config
from common.utils.mapping_util import get_stock_name

fields = config.get_value('DAILY_FIELDS')


class PositionInfo:
    """
    持有的股票详情
    """

    def __init__(self, stock_code, stock_num, cost_price, trade_date):
        # 股票代码 stock code
        self._stock_code = stock_code
        # 股票名 stock name
        self._stock_name = get_stock_name(stock_code)
        # 股票数量 stock num
        self._stock_num = stock_num
        # 成本价格 cost price
        self._cost_price = cost_price
        # 交易日期
        self._trade_date = trade_date
        # 获取最新价格 latest_price
        cli = Client(stock_code, 7, fields)
        self._latest_price = cli.get_stock_df_daily()['close'].head(1).values[0]
        # 盈利率
        self._profit_rate = (self._latest_price - self._cost_price) / self._cost_price
        # 盈利金额
        self._profit = (self._latest_price - self._cost_price) * self._stock_num

    @property
    def stock_code(self):
        return self._stock_code

    @stock_code.setter
    def stock_code(self, value):
        self._stock_code = value

    @property
    def stock_name(self):
        return self._stock_name

    @stock_name.setter
    def stock_name(self, value):
        self._stock_name = value

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
    def cost_price(self):
        return self._cost_price

    @cost_price.setter
    def cost_price(self, value):
        if value < 0:
            raise ValueError('price must > 0 !')
        self._cost_price = value

    @property
    def trade_date(self):
        return self._trade_date

    @trade_date.setter
    def trade_date(self, value):
        self._trade_date = value

    @property
    def latest_price(self):
        return self._latest_price

    @latest_price.setter
    def latest_price(self, value):
        if value < 0:
            raise ValueError('price must > 0 !')
        self._latest_price = value

    @property
    def profit_rate(self):
        return self._profit_rate

    @profit_rate.setter
    def profit_rate(self, value):
        self._profit_rate = value

    @property
    def profit(self):
        return self._profit

    @profit.setter
    def profit(self, value):
        self._profit = value

    def __str__(self):
        return 'stock code: {}, stock name: {}, cost price: {}, latest price: {}, num: {}, profit rate: {:.2%}, profit: {}, trade date: {}'.format(
            self._stock_code, self._stock_name, self._cost_price, self._latest_price, self._stock_num,
            self._profit_rate, self._profit, self._trade_date)
