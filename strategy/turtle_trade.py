import math

import common.quotation.indicator as indicator
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
    def check_enter(ts_code, df, threshold=20):
        log.info('---- 获取入市时机: {} ----'.format(ts_code))
        if df is None:
            return False

        # 按时间升序
        df = df[::-1]
        max_price = 0
        df = df.tail(n=threshold)
        if len(df) < threshold:
            return False
        for index, row in df.iterrows():
            if row['close'] > max_price:
                max_price = float(row['close'])

        last_close = df.iloc[-1]['close']

        log.info('区间 %d 天内的高位是: %0.2f', threshold, max_price)
        if last_close >= max_price:
            return True

        return False

    # 最后一个交易日收市价为指定区间内最低价
    @staticmethod
    def check_exit(ts_code, df, threshold=5):
        log.info('---- 获取退出时机: {} ----'.format(ts_code))
        if df is None:
            return False

        # 按时间升序
        df = df[::-1]
        min_price = 99999
        df = df.tail(n=threshold)
        if len(df) < threshold:
            log.debug("{0}:样本小于{1}天...\n".format(ts_code, threshold))
            return False
        for index, row in df.iterrows():
            if row['close'] < min_price:
                min_price = float(row['close'])

        last_close = df.iloc[-1]['close']

        log.info('区间 %d 天内的低位是: %0.2f', threshold, min_price)
        if last_close <= min_price:
            return True

        return False

    # 止损, 达到总账户一定比略的亏损, 要考虑退出
    def check_stop(self, ts_code, df, position_df, stop_loss=0.1):
        """
        :param ts_code: 股票名字
        :param df: 股票的数据
        :param position_df: 对应股票的持仓数据
        :param stop_loss: 亏损达到账户总额的比率
        :return:
        """
        log.info('---- 获取止损时机: {} ----'.format(ts_code))
        if df is None:
            return False

        # 按时间升序
        df = df[::-1]

        last_close = df.iloc[-1]['close']
        positions = position_df['positions']
        cost = position_df['cost']
        current_cap = 0
        for (position_price, position_size) in positions:
            current_cap += position_size * last_close * 100

        log.info('持仓成本: %0.2f, 持仓现总价: %0.2f', cost, current_cap)
        # 持仓成本, 相对总账本亏损的承受度金额, 现在持仓的价格
        if cost - self._balance * stop_loss > current_cap:
            return True
        return False

    # 绝对波动幅度
    @staticmethod
    def real_atr(n, amount):
        return n * amount

    # 这个是计算买入头寸并保存
    def calc_buy(self, ts_code, df, threshold=14):
        log.info('---- 计算并保存买入的股票数据: {} ----'.format(ts_code))
        if len(df) < threshold:
            log.debug("{0}:样本小于{1}天...\n".format(ts_code, threshold))
            return False

        # 按时间升序
        df = df[::-1]
        # get_atr_df 默认是把atr数据塞进去df, 所以要再取['atr'], 然后时间升序
        atr_df = df[::-1].copy()
        atr_list = indicator.get_atr_df(atr_df, threshold)['atr'][::-1]

        atr = atr_list.iloc[-1]
        last_close = df.iloc[-1]['close']
        # 头寸规模
        # todo _balance 应该要减去数据库持仓总数获取, 并保存数据库
        position_size = math.floor(self._balance / 100 / self.real_atr(atr, 100))
        t_shelve = ShelvePersistence()
        t_shelve.save_buy(ts_code, last_close, position_size)

        # last_close, position_size, atr
        result = (
            "N：{0}\n"
            "头寸规模：{1}手\n"
            "买入价格：{2:0.2f}，{3:0.2f}，{4:0.2f}，{5:0.2f}\n"
            "危险需要退出的价格：{6:0.2f}\n\n"
                .format(atr, position_size,
                        last_close,
                        last_close + atr,
                        last_close + atr * 2,
                        last_close + atr * 3,
                        last_close - atr * 2))
        return result

    # 计算减仓, 并保存, 达到减仓时机卖80%, 达到止损时机卖100%
    def calc_reduce(self, ts_code, df, position_rate=0.8):
        """
        :param ts_code: 股票代码
        :param df: 股票数据
        :param position_rate: 卖出股票的百分比
        :return:
        """
        log.info('---- 计算并保存卖出的股票数据: {} ----'.format(ts_code))
        if df is None:
            return False

        # 按时间升序
        df = df[::-1]
        last_close = df.iloc[-1]['close']
        # 保存数据
        t_shelve = ShelvePersistence()
        t_shelve.save_reduce(ts_code, last_close, position_rate)
        # todo self._balance 修改值, 保存数据库

        result = ("卖出头寸比例：{0:0.2f}, 卖出价格：{1:0.2f}".format(position_rate, last_close))
        return result
