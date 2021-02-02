from common.quotation.data_filter import Filter
from common.utils.logger import Logger

log = Logger(__name__).logger


def get_mapping_info(origin_df, mapping_df):
    name_list = []
    industry_list = []
    log.info('---- 正在匹配公司数据 ----')
    for _, row1 in origin_df.iterrows():
        for _, row2 in mapping_df.iterrows():
            if row1['ts_code'] == row2['ts_code']:
                name_list.append(row2['name'])
                industry_list.append(row2['industry'])
    origin_df['name'] = name_list
    origin_df['industry'] = industry_list

    return origin_df


# 根据公司stock code列表获取对应公司名dict
def get_stock_name_dict(stock_code_list, trade_date=None):
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_all_stocks(trade_date)
    mapping_dict = {}
    for _, row in info_df.iterrows():
        mapping_dict[row['ts_code']] = row['name']
    result_dict = {}
    for stock_code in stock_code_list:
        result_dict[stock_code] = mapping_dict.get(stock_code, '')
    return result_dict


# 根据公司stock code获取对应公司名
def get_stock_name(stock_code):
    cli = Filter()
    # 公司的详细信息
    info_df = cli.get_all_stocks()
    for _, row in info_df.iterrows():
        if row['ts_code'] == stock_code:
            return row['name']


if __name__ == '__main__':
    # 688777.SH
    # 688788.SH
    tmp_dict = get_stock_name('688777.SH')
    print(tmp_dict)
