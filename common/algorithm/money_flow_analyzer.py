import numpy as np

from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config

fields = config.get_value('DAILY_FIELDS')


# 找出资金流异动的股票
def analyse_money_flow_stocks(stock_list, data_period=20, slope=0):
    """
    :param stock_list: 需要计算的股票代码列表
    :param data_period: 计算数据的时间段
    :param slope: 计算一段时间内资金流总和的斜率, 越高, 越活跃
    :return:
    """
    result_list = []
    slope_list = []
    for stock in stock_list:
        cli = Client(stock, data_period * 1.5, fields)
        df = cli.get_money_flow_df()
        if not df.empty:
            # 按时间升序来展示
            df = df[::-1]
            # 将前面一段时间的资金净流入累加
            df['total_net'] = df['net_mf_amount'].cumsum(axis=0)
            df = df[-data_period:]
            x_data = []
            y_data = []
            negative_flag = False
            for _, df_row in df.iterrows():
                x_data.append(float(df_row['trade_date']))
                # 累计资金流出, 不处理
                if df_row['total_net'] < 0:
                    negative_flag = True
                y_data.append(df_row['total_net'])
            if negative_flag:
                continue
            # 得到多项式系数，按照阶数从高到低排列, 这里拟合一阶线性方程
            k = np.polyfit(x_data, y_data, 1)
            # 多项式方程
            # k[0] 斜率 大于0, 表示上升趋势
            if k[0] > slope:
                result_list.append(stock)
                slope_list.append(stock + ' : ' + str(k[0]))
    return result_list, slope_list
