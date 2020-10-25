import pandas as pd
import tushare as ts
from retrying import retry

from common.utils import data_saver as saver
from common.utils import date_util
from common.utils import yml_loader as config
from common.utils.logger import Logger

log = Logger(__name__).logger


class Filter:
    def __init__(self):
        global pro

        # 设置token
        ts.set_token(config.get_value('TOKEN'))
        pro = ts.pro_api()

        self.last_bus_day = date_util.get_last_bus_day()

    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_all_stocks(self):
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        log.info('---- 获取股票列表数据 ----')
        stock_list_name = saver.get_csv_data_name('stocks', 'all', end_date=self.last_bus_day)
        if saver.check_file_existed(stock_list_name):
            data_list = saver.read_from_csv(stock_list_name)
        else:
            data_list = pro.stock_basic(exchange='', list_status='L',
                                        fields='ts_code,symbol,name,area,industry,list_date')
            if len(data_list) != 0:
                saver.save_csv(data_list, stock_list_name)
        return data_list

    # 获取市值数据
    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_total_mv_df(self):
        log.info('---- 获取所有市值数据 ----')
        file_name = saver.get_csv_data_name('stock_info', 'total_mv', end_date=date_util.get_last_bus_day())
        if saver.check_file_existed(file_name):
            df = saver.read_from_csv(file_name)
        else:
            df = pro.daily_basic(ts_code='', trade_date=date_util.get_last_bus_day(),
                                 fields='ts_code,trade_date,turnover_rate,pe,total_mv')
            if len(df) != 0:
                saver.save_csv(df, file_name)
        return df

    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_filtered_stocks(self, pe=100, total_mv=1500000, turnover_rate=3):
        log.info('---- 筛选业绩好的公司 ----')
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        stock_name = saver.get_csv_data_name('stock_info', 'recommended', end_date=self.last_bus_day)
        if saver.check_file_existed(stock_name):
            df = saver.read_from_csv(stock_name)
        else:
            df = pro.daily_basic(ts_code='', trade_date=self.last_bus_day,
                                 fields='ts_code,trade_date,turnover_rate,pe,total_mv')
            # ---------------------------------------
            # 自定义过滤条件, pe 静态市盈率, total_mv 总市值, turnover_rate 换手率
            df = df.drop(
                df[(df['pe'] < 0) | (df['pe'] > pe) | (df['total_mv'] < total_mv) | (
                        df['turnover_rate'] < turnover_rate)].index)
            # ---------------------------------------
            # 删除有空NaN的行
            df = df.dropna(axis=0, how='any')

            if len(df) != 0:
                saver.save_csv(df, stock_name)
        return df

    # 沪深股通十大成交股
    @retry(wait_random_min=1000, wait_random_max=2000, stop_max_attempt_number=3)
    def get_top10_stocks(self, trade_date=None):
        log.info('---- 沪深股通十大成交股 ----')
        if trade_date is None:
            trade_date = self.last_bus_day
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        stock_name = saver.get_csv_data_name('stock_info', 'top10', end_date=trade_date)
        if saver.check_file_existed(stock_name):
            df = saver.read_from_csv(stock_name)
        else:
            sh_df = pro.hsgt_top10(trade_date=trade_date, market_type='1',
                                   fields='ts_code,trade_date,name,close,amount,net_amount')
            sz_df = pro.hsgt_top10(trade_date=trade_date, market_type='3',
                                   fields='ts_code,trade_date,name,close,amount,net_amount')
            frames = [sh_df, sz_df]
            df = pd.concat(frames)

            if len(df) != 0:
                saver.save_csv(df, stock_name)
        return df

    # 个股资金流向
    # 获取单日全部股票数据
    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_money_flow_stocks(self, trade_date=None):
        log.info('---- 个股资金流向 ----')
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        stock_name = saver.get_csv_data_name('stock_info', 'money_flow', end_date=self.last_bus_day)
        if saver.check_file_existed(stock_name):
            df = saver.read_from_csv(stock_name)
        else:
            if trade_date is None:
                trade_date = self.last_bus_day
            df = pro.moneyflow(trade_date=trade_date,
                               fields='ts_code,trade_date,net_mf_vol,net_mf_amount,buy_lg_amount,buy_elg_amount')

            if len(df) != 0:
                saver.save_csv(df, stock_name)
        return df

    # 判断股票资金持续流入的股票
    @staticmethod
    def is_capital_inflow_stock(money_flow_df, threshold, target_amount):
        log.info('---- 判断该段时间内资金是否持续流入 ----')
        if money_flow_df is None:
            log.info('---- data is empty ----')
            return False

        # 按时间升序
        money_flow_df = money_flow_df[::-1]
        df = money_flow_df.tail(n=threshold)
        if len(df) < threshold:
            return False
        # 计算该段时间内资金流入情况
        total_amount = 0
        for index, row in df.iterrows():
            total_amount += row['net_mf_amount']
        # 指定流入数量大于某个数才加入候选
        if total_amount >= target_amount:
            return True

        return False

    # 判断股票资金持续流入超过市值一定比例的股票
    @staticmethod
    def is_capital_inflow_percent_stock(money_flow_df, total_mv, threshold, target_percent):
        """
        判断股票资金持续流入是否超过市值一定比例
        :param money_flow_df: 资金流的df
        :param total_mv: 公司最近一天的总市值
        :param threshold: 时间段
        :param target_percent: 目标的百分比
        :return: bool值
        """
        # 计算一段时间内资金量流入占市值的%
        log.info('---- 判断该段时间内资金流入占市值比例 ----')
        if money_flow_df is None:
            log.info('---- data is empty ----')
            return False

        # 按时间升序
        money_flow_df = money_flow_df[::-1]
        df = money_flow_df.tail(n=threshold)
        if len(df) < threshold:
            return False
        # 计算该段时间内资金流入情况
        total_amount = 0
        for index, row in df.iterrows():
            total_amount += row['net_mf_amount']
        # 资金流入总量 / 总市值 >= 指定百分比
        if total_amount / total_mv >= target_percent:
            return True

        return False
