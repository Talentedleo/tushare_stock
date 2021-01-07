import numpy as np

import common.quotation.indicator as indicator
import common.utils.tool as tool
from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config

fields = config.get_value('DAILY_FIELDS')


# 找出atr异动的股票
def analyse_atr_stocks(stock_list, slope, slope_period=5, data_period=120):
    """
    :param stock_list: 需要计算的股票代码列表
    :param slope: 计算atr的斜率, 越高, 越活跃
    :param slope_period: 真正计算用的范围
    :param data_period: 一段时间的数据
    :return:
    """
    tool.show_all_df()
    result_dict = {}
    for stock in stock_list:
        cli = Client(stock, data_period, fields)
        stock_df = cli.get_stock_df_daily()
        # atr数据
        df = indicator.get_atr_df(stock_df)
        if not df.empty:
            # 按时间升序来展示
            df = df[::-1]
            df = df.tail(slope_period)
            x_data = []
            y_data = []
            for _, df_row in df.iterrows():
                x_data.append(float(df_row['trade_date']))
                y_data.append(df_row['atr'])
            # 得到多项式系数，按照阶数从高到低排列, 这里拟合一阶线性方程
            k = np.polyfit(x_data, y_data, 1)
            # 多项式方程
            # k[0] 斜率 大于0, 表示上升趋势
            if k[0] > slope:
                result_dict[stock] = k[0]
    # 按斜率倒排序 eg: [('600702.SH', 0.05652120048096933), ('600779.SH', 0.052775777742866826)]
    sorted_list = sorted(result_dict.items(), key=lambda it: it[1], reverse=True)
    return sorted_list


if __name__ == '__main__':
    analyse_atr_stocks(['601633.SH'], 1, 5)
