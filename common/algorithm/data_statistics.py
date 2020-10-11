import pandas as pd

from common.utils import date_util as date
from common.utils.logger import Logger

log = Logger(__name__).logger


# 统计data frame中的数据
def find_most_popular_stock(func, day_before=10, end_date=date.get_now_date(), top_num=10):
    df_list = []
    for i in range(day_before):
        day = i + 1
        # 通过字符串日期获取n天前的字符串日期
        trade_date = date.transform_str_date_ago(end_date, day)
        # 获取历史的df数据
        stock_df = func(trade_date)
        df_list.append(stock_df)
    # 将数据汇总
    total_df = pd.concat(df_list)
    # 先分组后统计数据
    calc_size_df = total_df.groupby(['ts_code', 'name']).size().reset_index(name='count')
    # 排序
    sort_df = calc_size_df.sort_values(by='count', ascending=False)[:top_num]
    log.info('最近 {} 天沪深十大成交股统计: top {}'.format(day_before, top_num))
    log.info(sort_df)
