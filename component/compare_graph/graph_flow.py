import component.filtered_stock.stock_chance as chance
from component.compare_graph.draw_component import DrawComponent


# 绘制 单个 图形
def draw_multi_graph_by_stock(stock):
    drawer = DrawComponent(stock, 120)

    drawer.get_atr_graph(5)
    #################################################
    # drawer.get_money_flow_graph(5)
    #################################################
    # drawer.get_turnover_graph(5)
    #################################################
    # drawer.get_amount_graph()
    #################################################
    # drawer.get_sma_graph()
    #################################################
    # drawer.get_index_compare_graph()


# 绘制 多个 图形
def draw_multi_graph_by_stock_list(stock_list):
    for stock in stock_list:
        draw_multi_graph_by_stock(stock)


# 绘制 沪深股通十大成交股 的图形
def draw_multi_graph_by_top10_company():
    top10_company_df = chance.get_top10_company()
    for company in top10_company_df['ts_code']:
        draw_multi_graph_by_stock(company)


if __name__ == '__main__':
    # todo 总结 选股后画图再次分析

    # 京东方A '000725.SZ'
    # 长城汽车 '601633.SH'
    # 美的集团 '000333.SZ'
    # TCL科技 '000100.SZ'
    # 比亚迪 '002594.SZ'

    # 东山精密 '002384.SZ'
    # 神州数码 '000034.SZ'
    # 安宁股份 '002978.SZ'
    # 桐昆股份 '601233.SH'
    # 赣锋锂业 '002460.SZ'
    # 隆基股份 '601012.SH'
    # 分众传媒 '002027.SZ'

    # 绘制 单个 股票图形
    draw_multi_graph_by_stock('000725.SZ')

    # 绘制 多个 股票图形
    # draw_multi_graph_by_stock_list(['000725.SZ', '601633.SH'])

    # 绘制 沪深股通十大成交股 的图形
    # draw_multi_graph_by_top10_company()