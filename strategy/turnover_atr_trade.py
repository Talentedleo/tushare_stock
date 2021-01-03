from common.algorithm.atr_analyzer import analyse_atr_stocks
from common.utils.mapping_util import get_stock_name_dict
from component.filtered_stock.stock_chance import find_turnover_stocks_data


# 将换手率结合atr数据来选股
def get_turnover_atr_rise_stocks(choice='high', turnover_slope=1, turnover_slope_period=5,
                                 atr_slope=0.5, atr_slope_period=5, data_period=120):
    """
    :param choice: 公司类型
    :param turnover_slope: 转手率的斜率
    :param turnover_slope_period: 转手率的数据长度
    :param atr_slope: atr的斜率
    :param atr_slope_period: atr斜率计算的时间段
    :param data_period: 用来计算atr的时间段
    :return:
    """
    result_list, _ = find_turnover_stocks_data(choice, turnover_slope_period, turnover_slope)
    potential_stocks = analyse_atr_stocks(result_list, atr_slope, atr_slope_period, data_period)
    print(potential_stocks)
    return potential_stocks


if __name__ == '__main__':
    # get_turnover_atr_rise_stocks('high', 1, 5, 0.035, 5)
    get_turnover_atr_rise_stocks('high', 1, 5, 0.015, 5)
