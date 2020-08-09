import common.graph.graph_drawer as graph
from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
import common.quotation.indicator as indicator
from common.utils import yml_loader as config
import talib as ta

if __name__ == '__main__':
    stock = config.get_value('STOCK')
    # stock_code = stock.get('STOCK_CODE')
    stock_code = '601377.SH'
    # days = stock.get('DAYS_INTERVAL')
    days = 365
    fields = stock.get('FIELDS')

    # print(help(ta.MA))

    cli = Client(stock_code, days, fields)
    stock_df = cli.get_stock_df_daily()

    # atr数据
    stock_df = indicator.get_atr_df(stock_df)
    graph.draw_field_compare_plot(stock_df, 'atr', '{} Stock Market'.format(stock_code), 20)

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
