# todo 股票编码 + 指定日期后一段时间内的涨跌情况统计
from common.quotation.data_wrapper import Client
from common.utils import date_util
from common.utils.logger import Logger

log = Logger(__name__).logger


# 观察指定日期之后, 股票价格涨跌情况
def check_timing_price(stock, stock_df, trade_date, observation_period=5):
    # 日期计算, 往后的日期
    # 起始日期推后一天, 因为当天不能买入, 用来分析
    start_date = date_util.transform_str_date_after(str(trade_date), 1)
    # 在已有的df数据筛选指定日期范围内的数据
    interval_df = stock_df.loc[(stock_df['trade_date'].apply(lambda x: int(x)) >= int(start_date))].head(
        observation_period)
    profit_rate = 0
    if len(interval_df) > 0:
        buy_price = interval_df.head(1)['close'].values[0]
        sell_price = interval_df.tail(1)['close'].values[0]
        profit_rate = (sell_price - buy_price) / buy_price
        log.info(
            '{}: buy price {}, sell price {}, profit rate {:.4%}'.format(stock, buy_price, sell_price, profit_rate))
    return profit_rate


# 计算所有关键日期的利润
def check_timing_list_price(stock_dict, observation_period=5):
    profit_dict = {}
    fields = 'ts_code,trade_date,close,high,low,vol,amount'
    for stock, timing_list in stock_dict.items():
        # 回测数据
        start_date = str(timing_list[0])
        end_date = date_util.get_now_date()
        # 区间内的df数据
        cli = Client(stock, 0, fields, start_date, end_date)
        stock_df = cli.get_stock_df_daily()
        # 升序
        stock_df = stock_df[::-1]
        profit_rate_list = []
        for trade_date in timing_list:
            # 逐个关键日期分析
            profit_rate = check_timing_price(stock, stock_df, trade_date, observation_period)
            # 利润率为0表示数据量为1, 不足以支撑计算
            if profit_rate != 0:
                profit_rate_list.append(profit_rate)
        # 所有关键日期的盈亏情况
        profit_dict[stock] = profit_rate_list
    return profit_dict


# 观察期内, 不再找机遇点, 删除机遇点密集的数据
def delete_observation_timing_date(stock_dict, observation_period=5):
    result_dict = {}
    # 总的限制日期, 防止数据量少, 不足以校验
    date_limit = int(date_util.transform_str_date_ago(date_util.get_now_date(), observation_period))
    for stock, timing_list in stock_dict.items():
        filtered_list = [timing_list[0]]
        slide_variable = timing_list[0]
        for timing in timing_list[1:]:
            # 获取排序的区间段的数据
            if (int(timing) > (int(slide_variable) + observation_period)) & (int(timing) <= date_limit):
                filtered_list.append(timing)
                slide_variable = timing
        result_dict[stock] = filtered_list
    return result_dict


if __name__ == '__main__':
    test_dict = {'002384.SZ': [20201109]}
    for stock_code, key_timing_list in test_dict.items():
        # 回测数据
        check_timing_list_price(stock_code, key_timing_list, 3)