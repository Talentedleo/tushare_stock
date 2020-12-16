import math
import time

import pandas as pd

import common.algorithm.money_flow_analyzer as money_analyzer
import common.algorithm.turnover_analyzer as turnover_analyzer
import common.quotation.indicator as indicator
import common.utils.tool as tool
from common.algorithm.data_statistics import find_most_popular_stock
from common.algorithm.zone_analyzer import check_new_high
from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
from common.utils import date_util as date
from common.utils import mapping_util
from common.utils.logger import Logger
from component.compare_graph.draw_component import DrawComponent
import component.back_testing.data_back_testing as back_testing
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
def get_good_company_list(pe=100, total_mv=1500000, turnover_rate=3):
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_all_stocks()
    # 筛选一波好的公司
    record_df = cli.get_filtered_stocks(pe, total_mv, turnover_rate)
    # 匹配公司信息
    record_df = mapping_util.get_mapping_info(record_df, info_df)
    # 显示所有
    tool.show_all_df()
    log.info(record_df)


# 沪深股通十大成交股
def get_top10_company(trade_date=None):
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_top10_stocks(trade_date)
    # 显示所有列
    tool.show_all_df()
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
    :return: 筛选后的公司列表
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
        # 筛选流入资金是否超过指定的值
        target_flag = Filter.is_capital_inflow_stock(stock_df, days_interval, target_amount)
        if target_flag:
            show_list.append(company + ' ' + name + ' ' + industry)
            company_list.append(company)

    log.info('---- Companies with capital inflows of more than {} (ten thousand yuan) within {} days: ----'.format(
        target_amount, days_interval))
    log.info('---- recommended size: {} ----'.format(len(company_list)))
    for company_info in show_list:
        log.info('---- {} ----'.format(company_info))
    return company_list


# 拿到个股的历史资金流数据, 持续净流入超过市值一定比率就是有机会
def get_capital_inflow_stock_percent_list(df_days=120, days_interval=10, target_percent=0.1):
    """
    计算一段时间内资金流入和流出情况, 判断主力是否还在
    :param df_days: df的数据量
    :param days_interval: 计算资金流动的区间
    :param target_percent: 资金流入占市值比例目标值
    :return: 筛选后的公司列表
    """
    fields = 'ts_code,trade_date,close,high,low,vol,amount'

    fil = Filter()
    # 公司的详细信息
    info_df = fil.get_all_stocks()
    # 所有公司市值数据
    total_mv_df = fil.get_total_mv_df()
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
        # 获取指定公司当前的市值
        tmp_df = total_mv_df.loc[total_mv_df['ts_code'] == company]
        if not tmp_df.empty:
            total_mv = tmp_df['total_mv'].iloc[0]
            # 计算近段时间资金流入超过市值比例
            target_flag = Filter.is_capital_inflow_percent_stock(stock_df, total_mv, days_interval, target_percent)
            if target_flag:
                show_list.append(company + ' ' + name + ' ' + industry)
                company_list.append(company)

    log.info('---- Companies with ratio of capital flow to market value more than {}% within {} days: ----'.format(
        target_percent * 100, days_interval))
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


# [多天数据] 根据资金流获取有机会的公司 单位: 万元. 单纯比较总资金流入量
def draw_multi_company_capital_inflow_amount_graph(df_days=120, days_interval=10, target_amount=0, graph_length=120,
                                                   step=5):
    comp_list = get_capital_inflow_stock_list(df_days, days_interval, target_amount)
    new_df = pd.DataFrame()
    new_df['ts_code'] = comp_list
    # 绘图
    draw_stocks_money_flow_graph(new_df, graph_length, step)


# [多天数据] 根据资金流获取有机会的公司. 比较占总市值百分比
def draw_multi_company_capital_inflow_percent_graph(df_days=120, days_interval=10, target_percent=0.1, graph_length=120,
                                                    step=5):
    """
    :param df_days: 数据的时间长度
    :param days_interval: 比较的时间段
    :param target_percent: 目标百分比
    :param graph_length: 绘图的x轴数据长度
    :param step: 步长
    :return:
    """
    comp_list = get_capital_inflow_stock_percent_list(df_days, days_interval, target_percent)
    new_df = pd.DataFrame()
    new_df['ts_code'] = comp_list
    # 绘图
    draw_stocks_money_flow_graph(new_df, graph_length, step)


# [一天数据] 排名前面的个股资金流向
def draw_one_day_capital_inflow_graph(top_num=20, trade_date=None):
    stocks_df = get_money_flow_stocks(top_num, trade_date)
    # 绘制各股票一定时间段内资金流向图
    draw_stocks_money_flow_graph(stocks_df)


# 沪深股通十大成交股
def draw_sh_sz_top_graph(trade_date=None):
    stocks_df = get_top10_company(trade_date)
    # 绘制各股票一定时间段内资金流向图
    draw_stocks_money_flow_graph(stocks_df)


# 历史沪深股通十大成交股统计, 热门的股票
def find_sh_sz_popular_stocks(day_before=10, end_date=date.get_now_date(), top_num=10):
    # 取前10的数据
    find_most_popular_stock(get_top10_company, day_before, end_date, top_num)


# 分析高转手率有机会的股票
def find_turnover_stocks(choice='high', data_period=20, slope=0, graph_length=30, step=5):
    fil = Filter()
    if choice is 'high':
        # 优质公司
        stocks_df = fil.get_filtered_stocks()
    elif choice is 'const':
        # 沪深成分股
        stocks_df = fil.get_sh_sz_constituent_stock()
    else:
        # 所有公司
        stocks_df = fil.get_all_stocks()
    stock_list = stocks_df['ts_code'].tolist()
    # 符合条件的绘图, 斜率越高, 换手率越高, 股票越活跃
    result_list, slope_list = turnover_analyzer.analyse_turnover_stocks(stock_list, data_period, slope)
    for stock in result_list:
        # 绘图
        drawer = DrawComponent(stock, graph_length)
        drawer.get_turnover_graph(step)
        drawer.get_atr_graph(step)
    # 打印
    for stock_info in slope_list:
        log.info(stock_info)


# 分析累加资金流入有机会的股票
def find_money_flow_stocks(choice='high', data_period=20, slope=0, graph_length=30, step=5):
    fil = Filter()
    if choice is 'high':
        # 优质公司
        stocks_df = fil.get_filtered_stocks()
    elif choice is 'const':
        # 沪深成分股
        stocks_df = fil.get_sh_sz_constituent_stock()
    else:
        # 所有公司
        stocks_df = fil.get_all_stocks()
    stock_list = stocks_df['ts_code'].tolist()
    # 符合条件的绘图, 斜率越高, 换手率越高, 股票越活跃
    result_list, slope_list = money_analyzer.analyse_money_flow_stocks(stock_list, data_period, slope)
    for stock in result_list:
        # 绘图
        drawer = DrawComponent(stock, graph_length)
        drawer.get_accumulative_money_flow_graph(step)
    # 打印
    for stock_info in slope_list:
        log.info(stock_info)


# 搜索一段时间内历史高换手率的 股票 突破日期
def find_history_turnover_stocks(choice='high', total_period=120, data_section=5, slope=1, observation_period=5):
    fil = Filter()
    if choice is 'high':
        # 优质公司
        stocks_df = fil.get_filtered_stocks()
    elif choice is 'const':
        # 沪深成分股
        stocks_df = fil.get_sh_sz_constituent_stock()
    else:
        # 所有公司
        stocks_df = fil.get_all_stocks()
    stock_list = stocks_df['ts_code'].tolist()
    # 符合条件的绘图, 斜率越高, 换手率越高, 股票越活跃
    origin_dict = turnover_analyzer.analyse_history_timing(stock_list, total_period, data_section, slope)
    # 删除太密集的机遇点
    filtered_dict = back_testing.delete_observation_timing_date(origin_dict, observation_period)
    # 关键日期的利润
    profit_dict = back_testing.check_timing_list_price(filtered_dict, observation_period)
    # 打印结果
    log.info(filtered_dict)
    log.info(profit_dict)
    # 统计升跌情况
    stock_sum = 0
    rise = 0
    fall = 0
    rate_sum = 0
    for profit_list in profit_dict.values():
        for profit_rate in profit_list:
            if profit_rate > 0:
                rise += 1
            else:
                fall += 1
            stock_sum += 1
            rate_sum += profit_rate
    log.info('短期追热点 上涨比例: {:.4%}'.format(rise / stock_sum))
    log.info('短期追热点 下跌比例: {:.4%}'.format(fall / stock_sum))
    log.info('短期追热点 平局利润率: {:.4%}'.format(rate_sum))
    log.info('短期追热点 买100000元平均盈利: {}'.format(100000 * rate_sum))


if __name__ == '__main__':
    # todo 总结 数据选股(首先要大盘是牛市)

    # 搜索一段时间内历史高换手率的 股票 突破日期 观察天数选5天或者6天
    # find_history_turnover_stocks('high', 60, 5, 1, 5)

    # 搜索高换手率的股票, 寻找机会, 可以修改slope斜率参数(注意, 也可能是庄家逃离!)
    # data_period 应该为7, 因为有周末2天占了数据
    find_turnover_stocks('const', 7, 1, 60, 5)

    # 搜索资金流持续流入的股票, 寻找机会
    # find_money_flow_stocks('high', 5, 1, 10, 2)

    # [多天数据] 根据资金流获取有机会的公司 单位: 万元, 资金流入超过市值一定比率.
    # draw_multi_company_capital_inflow_percent_graph(60, 5, 0.02, 60, 5)

    # [多天数据] 根据资金流获取有机会的公司 单位: 万元, 单纯比较总资金流入量. 5天内持续流入超2亿的股票
    # draw_multi_company_capital_inflow_amount_graph(60, 5, 20000, 60, 5)

    # [一天数据] 排名前面的个股资金流向
    # draw_one_day_capital_inflow_graph(20, '20201109')

    # 找出好公司列表
    # get_good_company_list(65, 2000000, 2)
    # get_good_company_list()

    # 沪深股通十大成交股
    # draw_sh_sz_top_graph('20201109')

    # 历史沪深股通十大成交股统计, 热门的股票, 这里是20天内的数据统计, 取最后结果的前10数据
    # find_sh_sz_popular_stocks(20, date.get_now_date(), 10)

    # 结论: 分红后跌多涨少! 统计分红后升跌
    # get_dividend_statistics(20200101, 1, 10)

    # 分红送股
    # get_dividend_info()

    # 找出一段时间内振荡或者下降的股票
    # first_chance_df = get_oscillation_stock(field='atr')
