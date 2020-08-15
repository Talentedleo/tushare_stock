from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
from common.utils import mapping_util
from common.utils import yml_loader as config
from strategy import oscillation_zone as strategy

if __name__ == '__main__':
    stock = config.get_value('STOCK')
    days = 60
    fields = stock.get('FIELDS')

    # 过滤后的公司, 使用区间震荡策略, 找到机会
    cli = Filter()
    info_df = cli.get_all_stocks()
    df = cli.get_filtered_stocks()
    recommend_list = []
    for company in df['ts_code']:
        cli = Client(company, days, fields)
        # 重试机制
        stock_df = cli.get_stock_df_daily()
        # stock_df = indicator.get_atr_df(stock_df)
        record_df = strategy.get_oscillation_zone_df(stock_df, 'close')
        # stock_df = cli.get_stock_df_weekly()
        # record = strategy.get_fall_down_dict(stock_df, 'close', 2)
        if record_df is not None:
            if len(record_df.index) > 0:
                record_df = mapping_util.get_mapping_info(record_df, info_df)
                recommend_list.append(record_df)

    for item in recommend_list:
        for index, row in item.iterrows():
            print(row['ts_code'], row['name'], row['industry'], row['trade_date'], row['close'])
