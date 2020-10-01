import pandas as pd

from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
import common.quotation.indicator as indicator
from common.utils.logger import Logger
from common.utils import mapping_util
from strategy import oscillation_zone as strategy

log = Logger(__name__).logger


def get_oscillation_stock(field='close', rate=0.0155, days=30, period=5):
    """
    获取推荐股票振荡区间的df, 只适合熊市中找机会
    :param rate: 波动率
    :param field: 用来计算的指标
    :param days: 总时间区间
    :param period: 筛选的区间段
    :return: 数据集
    """
    # 第一步, 过滤出最近下跌趋势的股票或者是区间稳定的股票
    # 过滤后的公司, 使用区间震荡策略, 找到机会
    fields = 'ts_code,trade_date,close,high,low,vol,amount'

    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_all_stocks()
    # 筛选一波好的公司
    df = cli.get_filtered_stocks()
    recommend_list = []
    for company in df['ts_code']:
        cli = Client(company, days, fields)
        # 重试机制
        stock_df = cli.get_stock_df_daily()
        # atr数据
        if field == 'atr':
            stock_df = indicator.get_atr_df(stock_df)
        # 在好的公司里面调用区域震荡策略
        record_df = strategy.get_oscillation_zone_df(stock_df, field, rate, period)
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
            log.info(
                '{} {} {} {} {}'.format(row['ts_code'], row['name'], row['industry'], row['trade_date'], row['close']))
    unique_df = unique_df['ts_code'].drop_duplicates()

    return unique_df


# 展示所有业绩好的公司
def get_good_company_list():
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_all_stocks()
    # 筛选一波好的公司
    record_df = cli.get_filtered_stocks()
    # 匹配公司信息
    record_df = mapping_util.get_mapping_info(record_df, info_df)
    # 显示所有列
    # pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 1000)
    log.info(record_df)


# 沪深股通十大成交股
def get_top10_company():
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_top10_stocks()
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 1000)
    log.info(info_df)


def get_money_flow_stocks():
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_money_flow_stocks()
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 1000)
    log.info(info_df)


if __name__ == '__main__':
    # 找出一段时间内振荡或者下降的股票
    # first_chance_df = get_oscillation_stock(field='atr')

    # 找出好公司列表
    # get_good_company_list()

    # 沪深股通十大成交股
    # get_top10_company()

    # 个股资金流向
    get_money_flow_stocks()
