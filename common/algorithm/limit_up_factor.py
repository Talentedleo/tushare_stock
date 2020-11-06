import pandas as pd

import common.utils.tool as tool
from common.quotation.data_filter import Filter
from common.utils.logger import Logger
from component.compare_graph.draw_component import DrawComponent

log = Logger(__name__).logger


# 多为小盘股或者新股, 没有研究的必要
# 分析涨跌停: 资金流 换手率 的关系
def analyse_limit_up_factors():
    limit_stocks_head_df = count_period_stocks_daily_limit(20)
    # 获取涨停的前20个数据
    limit_stocks_head_df = limit_stocks_head_df[:20]
    for ts_code in limit_stocks_head_df['ts_code']:
        drawer = DrawComponent(ts_code, 120)
        # 绘制资金流图
        # drawer.get_money_flow_graph(5)
        # 绘制换手率图, 换手率更明显
        drawer.get_turnover_graph(5)


# 统计一段时间内涨停股票的数目
def count_period_stocks_daily_limit(period=10):
    # 显示所有数据
    tool.show_all_df()
    fil = Filter()
    df = fil.get_period_limit_df(input_type='up', days=period)
    # 去除ST这样的危险股票
    df = df[~df.name.str.contains('ST')]
    # 先按名称分组
    total = pd.DataFrame({'total': df.groupby(['name', 'ts_code']).size()})
    # 倒排序
    total = total.sort_values(by='total', ascending=False)
    # 索引
    total.reset_index(inplace=True)
    log.info(total)
    return total


if __name__ == '__main__':
    # 统计一段时间内涨停股票的数目
    # count_period_stocks_daily_limit(15)

    # 分析涨跌停: 资金流 换手率 的关系
    analyse_limit_up_factors()
