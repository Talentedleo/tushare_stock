import tushare as ts
from retrying import retry

from common.utils import data_saver as saver
from common.utils import date_util
from common.utils.logger import Logger
from common.utils import yml_loader as config

log = Logger(__name__).logger


class Client:

    def __init__(self, stock_code, days_interval, fields):
        global pro

        # 设置token
        ts.set_token(config.get_value('TOKEN'))
        pro = ts.pro_api()

        self.stock_code = stock_code
        self.end_date = date_util.get_now_date()
        self.start_date = date_util.get_days_ago(days_interval)
        self.fields = fields

    def get_stock_df_daily(self):
        # 单个股票日数据
        log.info("---- 获取股票数据(日) ----")
        return self.get_stock_df('day')

    def get_stock_df_weekly(self):
        # 单个股票周数据
        log.info("---- 获取股票数据(周) ----")
        return self.get_stock_df('week')

    def get_stock_df_monthly(self):
        # 单个股票月数据
        log.info("---- 获取股票数据(月) ----")
        return self.get_stock_df('month')

    def get_index_df_daily(self):
        # 日指数
        # 动态获取股票对应市场: 上证综指, 深证成指
        log.info("---- 获取指数数据(日) ----")
        return self.get_index_df('day')

    def get_index_df_weekly(self):
        # 周指数
        # 动态获取股票对应市场: 上证综指, 深证成指
        log.info("---- 获取指数数据(周) ----")
        return self.get_index_df('week')

    def get_index_df_monthly(self):
        # 月指数
        # 动态获取股票对应市场: 上证综指, 深证成指
        log.info("---- 获取指数数据(月) ----")
        return self.get_index_df('month')

    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_stock_df(self, date):
        # 单个股票的数据
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        file_name = saver.get_csv_name(date, self.stock_code, self.start_date, self.end_date)
        if saver.check_file_existed(file_name):
            log.info('---- 读取csv数据 ----')
            df = saver.read_from_csv(file_name)
        else:
            if date == 'month':
                df = pro.monthly(ts_code=self.stock_code, start_date=self.start_date, end_date=self.end_date,
                                 fields=self.fields)
            elif date == 'week':
                df = pro.weekly(ts_code=self.stock_code, start_date=self.start_date, end_date=self.end_date,
                                fields=self.fields)
            else:
                df = pro.daily(ts_code=self.stock_code, start_date=self.start_date, end_date=self.end_date,
                               fields=self.fields)
            log.info('---- 保存csv数据 ----')
            if len(df) != 0:
                saver.save_csv(df, file_name)
        return df

    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_index_df(self, date):
        # 沪深大盘指数
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        if self.stock_code.endswith('SH'):
            index_code = '000001.SH'
        else:
            index_code = '399001.SZ'

        file_name = saver.get_csv_name(date, index_code, self.start_date, self.end_date)
        if saver.check_file_existed(file_name):
            log.info('---- 读取csv数据 ----')
            df = saver.read_from_csv(file_name)
        else:
            if date == 'month':
                df = pro.index_monthly(ts_code=index_code, start_date=self.start_date, end_date=self.end_date,
                                       fields=self.fields)
            elif date == 'week':
                df = pro.index_weekly(ts_code=index_code, start_date=self.start_date, end_date=self.end_date,
                                      fields=self.fields)
            else:
                df = pro.index_daily(ts_code=index_code, start_date=self.start_date, end_date=self.end_date,
                                     fields=self.fields)
            log.info('---- 保存csv数据 ----')
            if len(df) != 0:
                saver.save_csv(df, file_name)
        return df

    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_stock_info_df(self):
        # 通用行情接口, 换手率tor，量比vr, 均线
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        file_name = saver.get_csv_name('stock_info', self.stock_code, self.start_date, self.end_date)
        if saver.check_file_existed(file_name):
            log.info('---- 读取csv数据 ----')
            df = saver.read_from_csv(file_name)
        else:
            # 换手率tor，量比vr, 均线
            df = ts.pro_bar(ts_code=self.stock_code, start_date=self.start_date, end_date=self.end_date,
                            factors=['tor', 'vr'], ma=[5, 20, 60])
            log.info('---- 保存csv数据 ----')
            if len(df) != 0:
                saver.save_csv(df, file_name)
        return df
