import math

import numpy

import common.quotation.indicator as indicator
import common.utils.date_util as date
from common.utils.db import ShelvePersistence
from common.utils.logger import Logger

log = Logger(__name__).logger


class Turtle:
    def __init__(self, balance=100000):
        log.info('---- 调用海龟投资策略 ----')
        # 设置账户总额
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    # 最后一个交易日收市价为指定区间内最高价(突破区间高价就是买入点)
    @staticmethod
    def check_enter(ts_code, df, end_date=date.get_now_date(), threshold=60):
        log.info('---- 获取入市时机: {} ----'.format(ts_code))
        # 按时间升序
        df = df[::-1]

        max_price = 0
        if end_date is not None:
            mask = (df['trade_date'] <= int(end_date))
            df = df.loc[mask]
        if df is None:
            return False
        df = df.tail(n=threshold)
        if len(df) < threshold:
            return False
        for index, row in df.iterrows():
            if row['close'] > max_price:
                max_price = float(row['close'])

        last_close = df.iloc[-1]['close']

        if last_close >= max_price:
            return True

        return False

    # 最后一个交易日收市价为指定区间内最低价
    @staticmethod
    def check_exit(ts_code, df, end_date=date.get_now_date(), threshold=10):
        log.info('---- 获取退出时机: {} ----'.format(ts_code))
        # 按时间升序
        df = df[::-1]

        if df is None:
            return True
        min_price = 9999
        if end_date is not None:
            mask = (df['trade_date'] <= int(end_date))
            df = df.loc[mask]
        df = df.tail(n=threshold)
        if len(df) < threshold:
            log.debug("{0}:样本小于{1}天...\n".format(ts_code, threshold))
            return False
        for index, row in df.iterrows():
            if row['close'] < min_price:
                min_price = float(row['close'])

        last_close = df.iloc[-1]['close']

        if last_close <= min_price:
            return True

        return False

    # 止损
    def check_stop(self, ts_code, df, position_df, stop_loss=0.05):
        """
        :param ts_code: 股票名字
        :param df:
        :param position_df:
        :param stop_loss: 亏损达到账户总额的比率
        :return:
        """
        log.info('---- 获取止损时机: {} ----'.format(ts_code))
        # 按时间升序
        df = df[::-1]

        if df is None:
            return True
        last_close = df.iloc[-1]['close']
        positions = position_df['positions']
        cost = position_df['cost']
        current_cap = 0
        for (position_price, position_size) in positions:
            current_cap += position_size * last_close * 100

        if cost - self._balance * stop_loss > current_cap:
            return True
        return False

    # 绝对波动幅度
    @staticmethod
    def real_atr(n, amount):
        return n * amount

    def calculate(self, ts_code, df, end_date=date.get_now_date(), threshold=20):
        # 按时间升序
        df = df[::-1]

        begin_date = df.iloc[0]['trade_date']
        print(type(begin_date))
        if end_date is not None and isinstance(begin_date, numpy.int64):
            if int(end_date) < begin_date:  # 该股票在end_date时还未上市
                log.debug("{}在{}时还未上市".format(ts_code, end_date))
                return False

        if end_date is not None and isinstance(begin_date, numpy.int64):
            mask = (df['trade_date'] <= int(end_date))
            df = df.loc[mask]

        if len(df) < threshold:
            log.debug("{0}:样本小于{1}天...\n".format(ts_code, threshold))
            return False

        # get_atr_df 默认是把atr数据塞进去df, 所以要再取['atr'], 然后时间升序
        atr_list = indicator.get_atr_df(df, threshold)['atr'][::-1]

        atr = atr_list.iloc[-1]
        last_close = df.iloc[-1]['close']
        # 头寸规模
        position_size = math.floor(self._balance / 100 / self.real_atr(atr, 100))
        t_shelve = ShelvePersistence()
        t_shelve.save(ts_code, last_close, position_size)

        # last_close, position_size, atr
        result = (
            "N：{0}\n"
            "头寸规模：{1}手\n"
            "买入价格：{2:0.2f}，{3:0.2f}，{4:0.2f}，{5:0.2f}\n"
            "退出价格：{6:0.2f}\n\n"
                .format(atr, position_size,
                        last_close,
                        last_close + atr,
                        last_close + atr * 2,
                        last_close + atr * 3,
                        last_close - atr * 2))
        return result
