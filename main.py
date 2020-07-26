import common.graph.graph_drawer as graph
from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config

if __name__ == '__main__':
    stock_code = config.get_value('STOCK_CODE')
    days = config.get_value('DAYS_INTERVAL')
    fields = config.get_value('FIELDS')

    cli = Client(stock_code, days, fields)

    stock_df = cli.get_stock_df_weekly()

    # print('---- 绘制股票折线图(周) ----')
    # graph.draw_default_plot(stock_df, '{} Stock Market'.format(stock_code))

    index_df = cli.get_index_df_weekly()
    print('---- 绘制股票和指数的比较图(周) ----')
    graph.draw_default_compare_plot(stock_df, index_df, '{} week data'.format(stock_code))
