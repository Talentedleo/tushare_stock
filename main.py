import common.graph.graph_drawer as graph
from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
import common.quotation.indicator as indicator
from common.utils import yml_loader as config
import talib as ta

if __name__ == '__main__':
    stock = config.get_value('STOCK')
    stock_code = stock.get('STOCK_CODE')
    days = stock.get('DAYS_INTERVAL')
    fields = stock.get('FIELDS')

    # print(help(ta.MA))

    cli = Client(stock_code, days, fields)
    stock_df = cli.get_stock_df_daily()

    stock_df = indicator.get_sma_df(stock_df)

    print(stock_df)

    # graph.draw_field_compare_plot(stock_df, 'sma', '{} Stock Market'.format(stock_code), 20)

    # graph.draw_default_plot(stock_df, '{} Stock Market'.format(stock_code))
    # stock_df['ma'] = ta.MA(stock_df['close'])
    # print(stock_df)
    # graph.draw_default_bar(stock_df, '{} Stock Market'.format(stock_code))
    # print('---- 绘制股票折线图(周) ----')
    # index_df = cli.get_index_df_weekly()
    # print('---- 绘制股票和指数的比较图(周) ----')
    # graph.draw_default_compare_plot(stock_df, index_df, '{} week data'.format(stock_code))

    # cli = Filter()
    # df = cli.get_filtered_stocks()
    # print(df)
