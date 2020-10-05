import pandas as pd

from common.algorithm.zone_analyzer import check_new_high
from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
import common.quotation.indicator as indicator
from common.utils.logger import Logger
from common.utils import mapping_util
from common.utils import date_util as date
from strategy import oscillation_zone as strategy
from component.compare_graph.draw_component import DrawComponent
import time
import math

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
def get_top10_company(trade_date=None):
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_top10_stocks(trade_date)
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 1000)
    log.info(info_df)
    return info_df


# 找出资金流入前20的公司
def get_money_flow_stocks(head_num=20, trade_date=None):
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_all_stocks()
    # 资金流数据
    money_flow_df = cli.get_money_flow_stocks(trade_date)
    # 按净流入额倒排序, net_mf_amount
    money_flow_df.sort_values(by='net_mf_amount', ascending=False, inplace=True)
    # 提取前面的数据
    head_df = money_flow_df.head(n=head_num)
    # 匹配公司信息
    head_df = mapping_util.get_mapping_info(head_df, info_df)

    # 打印数据
    log.info('TS代码 公司 产业 日期 大单 特大单 净流入额')
    for _, item in head_df.iterrows():
        log.info(
            '{} {} {} {} {} {} {}万元'.format(item['ts_code'], item['name'], item['industry'], item['trade_date'],
                                            item['buy_lg_amount'], item['buy_elg_amount'], item['net_mf_amount']))
    return head_df


# 绘制特定股票列表的资金流图
def draw_stocks_money_flow_graph(stock_list_df, graph_length=120, step=5):
    for company in stock_list_df['ts_code']:
        drawer = DrawComponent(company, graph_length)
        drawer.get_money_flow_graph(step)
        # drawer.get_atr_graph(step)


# 拿到个股的历史资金流数据, 持续净流入的就有机会
def get_capital_inflow_stock_list(df_days=120, days_interval=10, target_amount=0):
    """
    计算一段时间内资金流入和流出情况, 判断主力是否还在
    :param df_days: df的数据量
    :param days_interval: 计算资金流动的区间
    :param target_amount: 累加资金目标值(单位: 万元)
    :return: 筛选后的公司列表1
    """
    fields = 'ts_code,trade_date,close,high,low,vol,amount'

    fil = Filter()
    # 公司的详细信息
    info_df = fil.get_all_stocks()
    show_list = []
    company_list = []
    for _, df_row in info_df.iterrows():
        # 接口限制: 每分钟最多访问该接口300次
        # time.sleep(0.25)
        company = df_row['ts_code']
        name = df_row['name']
        industry = df_row['industry']
        cli = Client(company, df_days, fields)
        stock_df = cli.get_money_flow_df()
        target_flag = Filter.is_capital_inflow_stock(stock_df, days_interval, target_amount)
        if target_flag:
            show_list.append(company + ' ' + name + ' ' + industry)
            company_list.append(company)

    log.info('---- Companies with capital inflows of more than {} (ten thousand yuan) within {} days: ----'.format(
        days_interval, target_amount))
    log.info('---- recommended size: {} ----'.format(len(company_list)))
    for company_info in show_list:
        log.info('---- {} ----'.format(company_info))
    return company_list


# 获取所有公司当年的分红送股信息, 计算分红日前后估价波动情况
def get_dividend_info(today=int(date.get_now_date())):
    """
    :param today: 只统计这个日期后的分红
    :return: 所有公司分红df
    """
    fil = Filter()
    # 公司的详细信息
    info_df = fil.get_all_stocks()

    total_dividend_df = pd.DataFrame()
    for company in info_df['ts_code']:
        cli = Client(company, 0, '')
        # 各公司的分红
        df = cli.get_dividend_df()
        for _, df_row in df.iterrows():
            record_date = df_row['record_date']
            div_proc = df_row['div_proc']
            # 非空
            if record_date is not None:
                # 有可能是字符串, 要转float
                if isinstance(record_date, str):
                    record_date = float(record_date)
                if not math.isnan(record_date):
                    # 筛选年份为 '今年' 的分红 而且为 '实施'
                    if record_date > today and div_proc == '实施':
                        total_dividend_df = total_dividend_df.append(df_row, ignore_index=True)
    # 日志记录
    log.info(total_dividend_df)
    return total_dividend_df


# 结论: 分红后跌多涨少! 统计分红后的升跌
def get_dividend_statistics(day=int(date.get_now_date()), before_day=2, after_day=10):
    dividend_df = get_dividend_info(day)
    rise_count = 0
    fall_count = 0
    total_count = 0
    for _, df_row in dividend_df.iterrows():
        try:
            # 检查数据 涨跌
            flag = check_new_high(df_row['ts_code'], df_row['record_date'], before_day, after_day)
            if flag:
                rise_count += 1
            else:
                fall_count += 1
            total_count += 1
        except Exception:
            log.error('---- calc error ----')
            continue
    log.info('rise percent: {}%'.format((rise_count / total_count) * 100))
    log.info('fall percent: {}%'.format((fall_count / total_count) * 100))


if __name__ == '__main__':
    # 结论: 分红后跌多涨少! 统计分红后升跌
    # get_dividend_statistics(20200101, 1, 10)

    # 分红送股
    get_dividend_info()

    # 多天数据 根据资金流获取有机会的公司 单位: 万元. 5天内持续流入超2亿的股票
    # comp_list = get_capital_inflow_stock_list(60, 5, 20000)
    # new_df = pd.DataFrame()
    # new_df['ts_code'] = comp_list
    # # 绘图
    # draw_stocks_money_flow_graph(new_df, 60, 5)

    # 一天数据 排名前面的个股资金流向
    # stocks_df = get_money_flow_stocks(20, '20200930')
    # 绘制各股票一定时间段内资金流向图
    # draw_stocks_money_flow_graph(stocks_df)

    # 找出一段时间内振荡或者下降的股票
    # first_chance_df = get_oscillation_stock(field='atr')

    # 找出好公司列表
    # get_good_company_list()

    # 沪深股通十大成交股
    # stocks_df = get_top10_company('20200930')
    # 绘制各股票一定时间段内资金流向图
    # draw_stocks_money_flow_graph(stocks_df)
