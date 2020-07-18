import tushare as ts
import pandas as pd
from config import TOKEN

# 设置token
ts.set_token(TOKEN)
# 设置打印完整性
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

pro = ts.pro_api()

if __name__ == '__main__':
    # 京东方A行情
    df = pro.daily(ts_code='000725.SZ', start_date='20191226', end_date='20191226')

    print("京东方A行情是:")
    print(df)
    print("*" * 100)
    print(df.get("open"))
