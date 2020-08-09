import common.graph.graph_drawer as graph
from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
import common.quotation.indicator as indicator
from common.utils import yml_loader as config
from strategy import breakthrough as strategy
import talib as ta
import time

if __name__ == '__main__':
    stock = config.get_value('STOCK')
    # stock_code = stock.get('STOCK_CODE')
    # stock_code = '601377.SH'
    # days = stock.get('DAYS_INTERVAL')
    days = 30
    fields = stock.get('FIELDS')

    # print(help(ta.MA))

    # cli = Client(stock_code, days, fields)
    # stock_df = cli.get_stock_df_daily()

    # atr数据
    # stock_df = indicator.get_atr_df(stock_df)
    # graph.draw_field_compare_plot(stock_df, 'atr', '{} Stock Market'.format(stock_code), 10)

    # 下降突破策略
    # 获取过滤后的公司
    cli = Filter()
    df = cli.get_filtered_stocks()
    recommend_list = []
    for company in df['ts_code']:
        cli = Client(company, days, fields)
        # 重试机制
        for _ in range(5):
            try:
                stock_df = cli.get_stock_df_daily()
                break
            except KeyError:
                time.sleep(1)
                print("Timeout Error")

        stock_df = indicator.get_atr_df(stock_df)
        record = strategy.get_fall_down_dict(stock_df, 'atr', 3)
        if record is not None:
            recommend_list.append(record)

    for dict in recommend_list:
        if len(dict) > 0:
            for value in dict.values():
                print(value['ts_code'], value['trade_date'], value['close'], value['atr'])

    # record = strategy.get_breakthrough_dict(stock_df, 'atr', 5)
    # for value in record.values():
    #     print(value['trade_date'], value['close'], value['atr'])
    #     print('*' * 50)

    # sma数据
    # stock_df = indicator.get_sma_df(stock_df)
    # graph.draw_field_compare_plot(stock_df, 'sma', '{} Stock Market'.format(stock_code), 20)

    # 成交量情况
    # graph.draw_default_compare_plot_bar(stock_df, '{} Stock Market'.format(stock_code), 30)

    # 换手率
    # stock_df = cli.get_stock_info_df()
    # graph.draw_field_compare_plot_bar(stock_df, 'turnover_rate', '{} Stock Market'.format(stock_code), 2)
    # graph.draw_default_compare_plot_bar(stock_df, '{} Stock Market'.format(stock_code), 2)

    # 和大盘走势比较
    # index_df = cli.get_index_df_daily()
    # print('---- 绘制股票和指数的比较图(周) ----')
    # graph.draw_default_compare_plot(stock_df, index_df, '{} week data'.format(stock_code))

    # 获取过滤后的公司
    # cli = Filter()
    # df = cli.get_filtered_stocks()
    # print(df)
