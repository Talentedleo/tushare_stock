import numpy as np

import common.utils.tool as tool
from common.quotation.data_wrapper import Client


# 找出换手率异动的股票
def analyse_turnover_stocks(stock_list, data_period=20, slope=0):
    """
    :param stock_list: 需要计算的股票代码列表
    :param data_period: 计算数据的时间段
    :param slope: 计算换手率的斜率, 越高, 越活跃
    :return:
    """
    tool.show_all_df()
    fields = 'ts_code,trade_date,close,high,low,vol,amount'
    result_list = []
    slope_list = []
    for stock in stock_list:
        cli = Client(stock, data_period, fields)
        df = cli.get_stock_info_df()
        if not df.empty:
            # 按时间升序来展示
            df = df[::-1]
            x_data = []
            y_data = []
            for _, df_row in df.iterrows():
                x_data.append(float(df_row['trade_date']))
                y_data.append(df_row['turnover_rate'])
            # 得到多项式系数，按照阶数从高到低排列, 这里拟合一阶线性方程
            k = np.polyfit(x_data, y_data, 1)
            # 多项式方程
            # k[0] 斜率 大于0, 表示上升趋势
            if k[0] > slope:
                result_list.append(stock)
                slope_list.append(stock + ' : ' + str(k[0]))
    return result_list, slope_list


if __name__ == '__main__':
    stock_tmp_list = ['000725.SZ', '002384.SZ']
    analyse_turnover_stocks(stock_tmp_list)
