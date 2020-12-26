from common.quotation.data_wrapper import Client


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
            fields = 'ts_code,trade_date,close,high,low,vol,amount'
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


if __name__ == '__main__':
    # 京东方A '000725.SZ'
    stock = Position('000725.SZ', 100, 5.5)
    print(stock.stock_code)
