from common.quotation.data_wrapper import Client
from common.utils.db import ShelvePersistence
from common.utils.logger import Logger
from strategy.turtle_trade import Turtle

log = Logger(__name__).logger


class TurtleWorkFlow:
    def __init__(self, stock_code='000725.SZ', days=365, balance=100000):
        # 准备工作
        self.stock_code = stock_code
        self.days = days
        self.fields = 'ts_code,trade_date,close,high,low,vol,amount'
        self.cli = Client(self.stock_code, self.days, self.fields)
        # 日数据
        self.stock_df = self.cli.get_stock_df_daily()
        # 海龟策略
        self.turtle = Turtle(balance)

    # 获取前些天的df数据
    def get_earlier_df(self, days=1):
        return self.stock_df[days:]

    @staticmethod
    def check_position():
        # 查询头寸
        ShelvePersistence.positions()

    def check_enter(self, ts_df, threshold=20):
        # 查询买入时机
        enter_flag = self.turtle.check_enter(self.stock_code, ts_df, threshold)
        log.info('enter? {}'.format(enter_flag))
        return enter_flag

    def check_stop(self, ts_df):
        # 查询止损时机
        with ShelvePersistence.open() as file:
            for key in file:
                code = file[key]['ts_code']
                if code == self.stock_code:
                    # 查询止损时机
                    stop_flag = self.turtle.check_stop(code, ts_df, file[key])
                    log.info('stop? {}'.format(stop_flag))
                    return stop_flag

    def check_exit(self, ts_df, threshold=5):
        # 查询减仓时机
        exit_flag = self.turtle.check_exit(self.stock_code, ts_df, threshold)
        log.info('exit? {}'.format(exit_flag))
        return exit_flag

    def save_buy(self, ts_df):
        # 买入并保存
        result = self.turtle.calc_buy(self.stock_code, ts_df)
        log.info('buy? {}'.format(result))

    def save_sell(self, ts_df, sell_rate=0.8):
        # 卖出并保存
        result = self.turtle.calc_reduce(self.stock_code, ts_df, sell_rate)
        log.info('sale? {}'.format(result))

    def check_cost(self, ts_df):
        cost = self.turtle.check_cost(self.stock_code, ts_df)
        log.info('**目前持仓 {} 的市值是: {}'.format(self.stock_code, cost))
        return cost


if __name__ == '__main__':
    # 兴业证券 '601377.SH'
    # 京东方A '000725.SZ'
    # 格力 '000651.SZ'
    # 广发证券 '000776.SZ'
    # 科大讯飞 '002230.SZ'
    # 永辉超市 '601933.SZ'
    balance = 100000
    wf = TurtleWorkFlow('601988.SZ', 365, balance)
    day = 90
    exit_time = 0
    stop_time = 0
    total_profit = 0
    # 模拟最近 day 天, 使用海龟策略的利润情况
    for i in reversed(range(day)):
        log.info('%d 天前的数据', i + 1)
        df = wf.get_earlier_df(i + 1)
        if wf.check_enter(df):
            wf.save_buy(df)
        # 减仓
        if wf.check_exit(df, 10):
            if exit_time == 0:
                wf.save_sell(df)
                exit_time += 1
            elif exit_time == 1:
                # 全部清空
                wf.save_sell(df, 1)
                exit_time = 0
        # 止损
        if wf.check_stop(df):
            if stop_time == 0:
                wf.save_sell(df)
                stop_time += 1
            elif stop_time == 1:
                # 全部清空
                wf.save_sell(df, 1)
                stop_time = 0
    wf.check_position()
    # 当前账户持股市值
    now_cost = wf.check_cost(wf.stock_df)
    # 总的账户利润
    wallet = wf.turtle.balance + now_cost - balance
    log.info('账户: {0:0.2f}'.format(wf.turtle.balance))
    print('战果: {0:0.2f}'.format(wallet))
