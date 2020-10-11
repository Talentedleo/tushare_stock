import tushare as ts
from retrying import retry

from common.utils import data_saver as saver
from common.utils import date_util
from common.utils import yml_loader as config
from common.utils.logger import Logger

log = Logger(__name__).logger


class Domestic_Economy:
    def __init__(self):
        global pro

        # 设置token
        ts.set_token(config.get_value('TOKEN'))
        pro = ts.pro_api()
        self.quarter_date = date_util.get_quarter_date()

    @retry(wait_random_min=1000, wait_random_max=2000, stop_max_attempt_number=3)
    def get_gdp_df(self, start_q=date_util.get_quarter_date_ago(365), end_q=date_util.get_quarter_date()):
        log.info('---- 获取国内GDP数据 ----')
        # 如果文件存在就读取已有的数据, 如果没有, 就缓存起来
        gdp_name = saver.get_csv_data_name('economy', 'domestic_gdp_', end_date=self.quarter_date)
        if saver.check_file_existed(gdp_name):
            df = saver.read_from_csv(gdp_name)
        else:
            df = pro.cn_gdp(start_q=start_q, end_q=end_q)
            # 获取指定字段
            # df = pro.us_tycr(start_q=start_q, end_q=end_q, fields='quarter,gdp,gdp_yoy')
            if len(df) != 0:
                saver.save_csv(df, gdp_name)
        return df


if __name__ == '__main__':
    # todo 总结 查看宏观经济情况

    cli = Domestic_Economy()
    gdp_df = cli.get_gdp_df(start_q=date_util.get_quarter_date_ago(730))
    print(gdp_df)
