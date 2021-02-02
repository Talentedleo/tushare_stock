import numpy as np

import common.utils.tool as tool
from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config

fields = config.get_value('DAILY_FIELDS')


# 找出换手率异动的股票
def analyse_turnover_stocks(stock_list, data_period=20, slope=0):
    """
    找出换手率异动的股票
    :param stock_list: 需要计算的股票代码列表
    :param data_period: 计算数据的时间段
    :param slope: 计算换手率的斜率, 越高, 越活跃
    :return:
    """
    tool.show_all_df()
    result_list = []
    slope_list = []
    for stock in stock_list:
        # 因为可能遇到周末, 数据量不够的情况, 需要再加几天
        cli = Client(stock, data_period + 5, fields)
        df = cli.get_stock_info_df()
        df = df[:data_period]
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
                slope_list.append(stock + ' ' + str(k[0]))
    return result_list, slope_list


# 找出一段时间内换手率异动的股票的所有时间点
def analyse_history_timing(stock_list, total_period=120, data_section=5, slope=1, start_date=None, end_date=None):
    """
    一段时间内换手率异动的股票的所有时间点
    :param stock_list: 股票列表
    :param total_period: 总时间区间
    :param data_section: 需要计算斜率的时间段
    :param slope: 换手率斜率
    :param start_date: 数据起始日期, 可为空
    :param end_date: 数据结束日期, 可为空
    :return:
    """
    tool.show_all_df()
    result_dict = {}
    for stock in stock_list:
        cli = Client(stock, total_period, fields, start_date, end_date)
        df = cli.get_stock_info_df()
        if not df.empty:
            # 按时间升序来展示
            df = df[::-1]

            df_length = len(df) - data_section
            # 一行一行偏移
            for i in range(df_length):
                last_index = i + data_section
                # 获取一个区间段的df数据
                df_section = df[i:last_index]

                x_data = []
                y_data = []
                for _, df_row in df_section.iterrows():
                    x_data.append(float(df_row['trade_date']))
                    y_data.append(df_row['turnover_rate'])
                # 得到多项式系数，按照阶数从高到低排列, 这里拟合一阶线性方程
                k = np.polyfit(x_data, y_data, 1)
                # 多项式方程
                # k[0] 斜率 大于0, 表示上升趋势
                if k[0] > slope:
                    timing_list = result_dict.get(stock, [])
                    # 获取日期数据
                    timing_list.append(df_section.tail(1)['trade_date'].values[0])
                    result_dict[stock] = timing_list
    return result_dict


if __name__ == '__main__':
    # stock_tmp_list = ['000725.SZ', '002384.SZ']
    # analyse_turnover_stocks(stock_tmp_list)

    stock_tmp_list = ['002384.SZ', '002978.SZ']
    analyse_history_timing(stock_tmp_list, 120, 5, 1)
