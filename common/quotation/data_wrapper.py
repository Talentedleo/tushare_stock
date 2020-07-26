import pandas as pd
import tushare as ts

from common.utils import data_saver as saver
from common.utils import date_util
from common.utils import yml_loader as config


class Client:

    def __init__(self, stock_code, days_interval, fields):
        global pro

        # 设置token
        ts.set_token(config.get_value('TOKEN'))
        # 设置打印完整性
        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)

        pro = ts.pro_api()

        self.stock_code = stock_code
        self.end_date = date_util.get_now_date()
        self.start_date = date_util.get_days_ago(days_interval)
        self.fields = fields

    def get_stock_df_daily(self):
        # 单个股票日数据
        print("---- 获取股票数据(日) ----")
        df = pro.daily(ts_code=self.stock_code, start_date=self.start_date, end_date=self.end_date,
                       fields=self.fields)

        self.save_read_cache_data('day', df)
        return df

    def get_stock_df_weekly(self):
        # 单个股票周数据
        print("---- 获取股票数据(周) ----")
        df = pro.weekly(ts_code=self.stock_code, start_date=self.start_date, end_date=self.end_date,
                        fields=self.fields)

        self.save_read_cache_data('week', df)
        return df

    def get_stock_df_monthly(self):
        # 单个股票月数据
        print("---- 获取股票数据(月) ----")
        df = pro.monthly(ts_code=self.stock_code, start_date=self.start_date, end_date=self.end_date,
                         fields=self.fields)
        self.save_read_cache_data('month', df)
        return df

    def get_index_df_daily(self):
        # 日指数
        # 动态获取股票对应市场: 上证综指, 深证成指
        print("---- 获取指数数据(日) ----")
        if self.stock_code.endswith('SH'):
            index_code = '000001.SH'
        else:
            index_code = '399001.SZ'

        df = pro.index_daily(ts_code=index_code, start_date=self.start_date, end_date=self.end_date,
                             fields=self.fields)
        self.save_read_cache_data('day', df)
        return df

    def get_index_df_weekly(self):
        # 周指数
        # 动态获取股票对应市场: 上证综指, 深证成指
        print("---- 获取指数数据(周) ----")
        if self.stock_code.endswith('SH'):
            index_code = '000001.SH'
        else:
            index_code = '399001.SZ'

        df = pro.index_weekly(ts_code=index_code, start_date=self.start_date, end_date=self.end_date,
                              fields=self.fields)
        self.save_read_cache_data('week', df)
        return df

    def get_index_df_monthly(self):
        # 月指数
        # 动态获取股票对应市场: 上证综指, 深证成指
        print("---- 获取指数数据(月) ----")
        if self.stock_code.endswith('SH'):
            index_code = '000001.SH'
        else:
            index_code = '399001.SZ'

        df = pro.index_monthly(ts_code=index_code, start_date=self.start_date, end_date=self.end_date,
                               fields=self.fields)
        self.save_read_cache_data('month', df)
        return df

    """
    如果文件存在就读取已有的数据, 如果没有, 就缓存起来
    """
    # todo 
    def save_read_cache_data(self, date, df):
        file_name = saver.get_csv_name(date, self.stock_code, self.start_date, self.end_date)
        if saver.check_file_existed(file_name):
            print('---- 读取csv数据 ----')
            saver.read_from_csv(file_name)
        else:
            print('---- 保存csv数据 ----')
            saver.save_csv(df, file_name)
