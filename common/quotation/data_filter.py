import tushare as ts

from common.utils import data_saver as saver
from common.utils import date_util
from common.utils import yml_loader as config


class Filter:
    def __init__(self):
        global pro

        # 设置token
        ts.set_token(config.get_value('TOKEN'))
        pro = ts.pro_api()

        self.last_bus_day = date_util.get_last_bus_day()

    def get_all_stocks(self):
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        stock_list_name = saver.get_csv_data_name('stocks', 'all', end_date=self.last_bus_day)
        if saver.check_file_existed(stock_list_name):
            print('---- 读取csv数据 ----')
            data_list = saver.read_from_csv(stock_list_name)
        else:
            data_list = pro.stock_basic(exchange='', list_status='L',
                                        fields='ts_code,symbol,name,area,industry,list_date')
            if len(data_list) != 0:
                saver.save_csv(data_list, stock_list_name)
        return data_list

    def get_filtered_stocks(self):
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        stock_name = saver.get_csv_data_name('stock_info', 'recommended', end_date=self.last_bus_day)
        if saver.check_file_existed(stock_name):
            print('---- 读取csv数据 ----')
            df = saver.read_from_csv(stock_name)
        else:
            df = pro.daily_basic(ts_code='', trade_date=self.last_bus_day,
                                 fields='ts_code,trade_date,turnover_rate,pe,total_mv')
            # ---------------------------------------
            # 自定义过滤条件, pe 静态市盈率, total_mv 总市值, turnover_rate 换手率
            df = df.drop(df[(df['pe'] > 100) | (df['total_mv'] < 1500000) | (df['turnover_rate'] < 5)].index)
            # ---------------------------------------
            # 删除有空NaN的行
            df = df.dropna(axis=0, how='any')

            if len(df) != 0:
                saver.save_csv(df, stock_name)
        return df
