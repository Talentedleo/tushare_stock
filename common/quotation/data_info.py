import tushare as ts
from retrying import retry

from common.utils import data_saver as saver
from common.utils import date_util
from common.utils import yml_loader as config


class BasicInfo:

    def __init__(self):
        global pro

        # 设置token
        ts.set_token(config.get_value('TOKEN'))
        pro = ts.pro_api()

        self.end_date = date_util.get_now_date()

    @retry(wait_random_min=1000, wait_random_max=2000)
    def get_stock_list(self):
        # 股票列表
        file_name = saver.get_csv_data_name('stock_info', 'stock_list', self.end_date)
        if saver.check_file_existed(file_name):
            print('---- 读取csv数据 ----')
            df = saver.read_from_csv(file_name)
        else:
            df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
            print('---- 保存csv数据 ----')
            if len(df) != 0:
                saver.save_csv(df, file_name)
        return df
