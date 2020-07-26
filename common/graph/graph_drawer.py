from matplotlib import pyplot as plt


# 绘制单张图
def draw_plot(x, y, x_label, title):
    plt.figure(figsize=(20, 8), dpi=80)
    plt.plot(range(len(x)), y)
    # x轴标签减少显示
    plt.xticks(range(0, len(x), 2), x_label[::2], rotation=45)
    # 网格显示
    plt.grid(alpha=0.4)
    plt.title(title)
    plt.show()


# 默认绘制效果图
def draw_default_plot(stock_df, title):
    x = stock_df['close'].index[::-1]
    y = stock_df['close'].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_plot(x, y, x_label, title)


# 绘制指定字段的折线图
def draw_field_plot(stock_df, field, title):
    x = stock_df[field].index[::-1]
    y = stock_df[field].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_plot(x, y, x_label, title)


# 分开两张图, 比较绘制
def draw_compare_plot(x1, y1, y2, x_label, title):
    plt.figure(figsize=(20, 8), dpi=80)
    fig, axs = plt.subplots(2, 1)
    # 绘制数据
    axs[0].plot(range(len(x1)), y1, alpha=0.7)
    axs[1].plot(range(len(x1)), y2, alpha=0.7)
    # y轴说明
    axs[0].set_ylabel('stock')
    axs[1].set_ylabel('index')
    # x轴标签减少显示
    plt.setp(axs, xticks=range(0, len(x1), 10), xticklabels=x_label[::10])
    # 网格显示
    axs[0].grid(alpha=0.4)
    axs[1].grid(alpha=0.4)

    fig.suptitle(title)
    plt.show()


# 默认比较折线图方法
def draw_default_compare_plot(stock_df, index_df, title):
    x1 = stock_df['close'].index[::-1]
    y1 = stock_df['close'].values[::-1]
    y2 = index_df['close'].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_compare_plot(x1, y1, y2, x_label, title)


# 绘制指定字段的比较折线图
def draw_field_compare_plot(stock_df, index_df, field, title):
    x1 = stock_df[field].index[::-1]
    y1 = stock_df[field].values[::-1]
    y2 = index_df[field].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_compare_plot(x1, y1, y2, x_label, title)

