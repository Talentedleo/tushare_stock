import common.graph.graph_drawer as graph
from common.quotation.data_filter import Filter
from common.utils import yml_loader as config
import talib as ta

if __name__ == '__main__':
    stock_code = config.get_value('STOCK_CODE')
    days = config.get_value('DAYS_INTERVAL')
    fields = config.get_value('FIELDS')

    # print(help(ta.MA))

    # cli = Client(stock_code, days, fields)
    # stock_df = cli.get_stock_df_weekly()
    # stock_df['ma'] = ta.MA(stock_df['close'])
    # print(stock_df)
    # graph.draw_default_bar(stock_df, '{} Stock Market'.format(stock_code))
    # print('---- 绘制股票折线图(周) ----')
    # graph.draw_default_plot(stock_df, '{} Stock Market'.format(stock_code))
    # index_df = cli.get_index_df_weekly()
    # print('---- 绘制股票和指数的比较图(周) ----')
    # graph.draw_default_compare_plot_bar(stock_df, '{} week data'.format(stock_code))

    cli = Filter()
    df = cli.get_filtered_stocks()
    # df = df.drop(df[(df.pe > 100) & (df.pe < 5)].index)
    print(df)
