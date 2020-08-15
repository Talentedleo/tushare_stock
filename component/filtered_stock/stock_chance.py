import pandas as pd

from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
from common.utils.logger import Logger
from common.utils import mapping_util
from strategy import oscillation_zone as strategy

log = Logger(__name__).logger


def get_oscillation_stock(days=30, period=5):
    # 第一步, 过滤出最近下跌趋势的股票或者是区间稳定的股票
    # 过滤后的公司, 使用区间震荡策略, 找到机会
    fields = 'ts_code,trade_date,close,high,low,vol,amount'

    cli = Filter()
    info_df = cli.get_all_stocks()
    df = cli.get_filtered_stocks()
    recommend_list = []
    for company in df['ts_code']:
        cli = Client(company, days, fields)
        # 重试机制
        stock_df = cli.get_stock_df_daily()
        record_df = strategy.get_oscillation_zone_df(stock_df, 'close', period)
        if record_df is not None:
            if len(record_df.index) > 0:
                # 匹配公司信息
                record_df = mapping_util.get_mapping_info(record_df, info_df)
                recommend_list.append(record_df)

    unique_df = pd.DataFrame()

    # 打印数据
    for item in recommend_list:
        unique_df = unique_df.append(item)
        for index, row in item.iterrows():
            log.info('{} {} {} {} {}'.format(row['ts_code'], row['name'], row['industry'], row['trade_date'], row['close']))
    unique_df = unique_df['ts_code'].drop_duplicates()

    return unique_df


if __name__ == '__main__':
    first_chance_df = get_oscillation_stock(30, 5)
