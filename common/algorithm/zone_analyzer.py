from common.quotation.data_wrapper import Client
import numpy as np


# 分红送股, 判断区间内数据是否上升
def check_new_high(ts_code, record_date, before_day, after_day):
    fields = 'ts_code,trade_date,close,high,low,vol,amount'
    record_date = int(record_date)
    # 记录日期前的一段时间
    start_date = record_date - before_day
    # 记录日期后的一段时间
    end_date = record_date + after_day
    cli = Client(ts_code, 0, fields, str(start_date), str(end_date))
    # 获取到一段时间内的df数据
    try:
        stock_df = cli.get_stock_df_daily()
    except Exception:
        return False
    # 判断非空
    if stock_df is None:
        return False
    # 按时间升序
    stock_df = stock_df[::-1]
    x_data = []
    y_data = []
    for _, df_row in stock_df.iterrows():
        x_data.append(float(df_row['trade_date']))
        y_data.append(df_row['close'])
    # 得到多项式系数，按照阶数从高到低排列, 这里拟合一阶线性方程
    k = np.polyfit(x_data, y_data, 1)
    # 多项式方程
    # formula = np.poly1d(k)
    # k[0] 斜率 大于0, 表示上升趋势
    if k[0] > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    # cli = Client('000725.SZ', 0, '')
    # # 各公司的分红
    # df = cli.get_dividend_df()
    # print(df)
    check_new_high('000725.SZ', 20200703.0, 1, 10)
