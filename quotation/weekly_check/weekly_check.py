import pandas as pd
import tushare as ts

import common.graph.graph_drawer as graph
from common.utils import yml_loader as config


def init():
    global pro

    # 设置token
    ts.set_token(config.get_value('TOKEN'))
    # 设置打印完整性
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)

    pro = ts.pro_api()


def get_stock_df(stock_code, start_date, end_date):
    # 京东方A行情
    return pro.weekly(ts_code=stock_code, start_date=start_date, end_date=end_date,
                      fields='ts_code,trade_date,close,vol,amount')


def get_index_df(index_code, start_date, end_date):
    # 周指数
    return pro.index_weekly(ts_code=index_code, start_date=start_date, end_date=end_date,
                            fields='ts_code,trade_date,close,vol,amount')


if __name__ == '__main__':
    print("---- 初始化 ----")
    init()

    stock_df = get_stock_df('000725.SZ', '20190719', '20200719')
    # graph.draw_default_plot(stock_df, 'Stock Market')

    # print("上证指数 周行情是:")
    index_df = get_index_df('000001.SH', '20190719', '20200719')
    graph.draw_default_compare_plot(stock_df, index_df, 'week data')
