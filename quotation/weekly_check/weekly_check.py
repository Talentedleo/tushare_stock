import tushare as ts
import pandas as pd
from common.utils import yml_loader as config

# 设置token
ts.set_token(config.get_value('TOKEN'))
# 设置打印完整性
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

pro = ts.pro_api()

if __name__ == '__main__':
    # 京东方A行情
    df = pro.weekly(ts_code='000725.SZ', start_date='20200601', end_date='20200715',
                    fields='ts_code,trade_date,open,high,low,close,vol,amount')

    print("京东方A 周行情是:")
    print(df)
