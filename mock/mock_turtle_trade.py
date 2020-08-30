from common.quotation.data_wrapper import Client
from common.utils.db import ShelvePersistence
from common.utils.logger import Logger
from strategy.turtle_trade import Turtle

log = Logger(__name__).logger


class TurtleWorkFlow:
    def __init__(self):
        # 准备工作
        self.stock_code = '000725.SZ'
        # stock_code = '601377.SH'
        self.days = 750
        self.fields = 'ts_code,trade_date,close,high,low,vol,amount'
        self.cli = Client(self.stock_code, self.days, self.fields)
        # 日数据
        self.stock_df = self.cli.get_stock_df_daily()
        # 海龟策略
        self.turtle = Turtle(100000)

    # 获取前些天的df数据
    def get_earlier_df(self, days=1):
        return self.stock_df[days:]

    @staticmethod
    def check_position():
        # 查询头寸
        ShelvePersistence.positions()

    def check_enter(self, ts_df):
        # 查询买入时机
        enter_flag = self.turtle.check_enter(self.stock_code, ts_df)
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

    def check_exit(self, ts_df):
        # 查询减仓时机
        exit_flag = self.turtle.check_exit(self.stock_code, ts_df)
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

    def check_profit(self, ts_df):
        profit = self.turtle.check_profit(self.stock_code, ts_df)
        log.info('**目前持仓 {} 的利润是: {}'.format(self.stock_code, profit))


if __name__ == '__main__':
    wf = TurtleWorkFlow()
    day = 720
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
        if wf.check_exit(df):
            if exit_time == 0:
                wf.save_sell(df)
                exit_time += 1
            elif exit_time == 1:
                # 全部清空
                wf.save_sell(df, 1)
                exit_time = 0
        # 止损
        # if wf.check_stop(df):
        #     if stop_time == 0:
        #         wf.save_sell(df)
        #         stop_time += 1
        #     elif stop_time == 1:
        #         # 全部清空
        #         wf.save_sell(df, 1)
        #         stop_time = 0
    log.info('查询账户')
    wf.check_position()
    wf.check_profit(wf.stock_df)
    # print()
