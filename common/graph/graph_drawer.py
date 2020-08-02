from matplotlib import pyplot as plt


# 绘制单张图
def draw_plot(x, y, x_label, title, step=2):
    plt.figure(figsize=(20, 8), dpi=80)
    plt.plot(range(len(x)), y)
    # x轴标签减少显示
    plt.xticks(range(0, len(x), step), x_label[::step], rotation=45)
    # 网格显示
    plt.grid(alpha=0.4)
    plt.title(title)
    plt.show()


# 条形图
def draw_bar(x, y, x_label, title, step=2):
    plt.figure(figsize=(20, 8), dpi=80)
    plt.bar(range(len(x)), y)
    plt.xticks(range(0, len(x), step), x_label[::step], rotation=45)
    plt.title(title)
    plt.show()


def draw_default_bar(stock_df, title, step=2):
    x = stock_df['amount'].index[::-1]
    y = stock_df['amount'].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_bar(x, y, x_label, title, step)


# 默认绘制效果图
def draw_default_plot(stock_df, title, step=2):
    x = stock_df['close'].index[::-1]
    y = stock_df['close'].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_plot(x, y, x_label, title, step)


# 绘制指定字段的折线图
def draw_field_plot(stock_df, field, title, step=2):
    x = stock_df[field].index[::-1]
    y = stock_df[field].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_plot(x, y, x_label, title, step)


# 同一张折线图, 多条折线
def draw_multiple_plot(x, y1, y2, x_label, y1_label, y2_label, title, step=2):
    plt.figure(figsize=(20, 8), dpi=80)
    plt.plot(range(len(x)), y1, label=y1_label, color='cyan')
    plt.plot(range(len(x)), y2, label=y2_label, color='red', linestyle='-.')
    # x轴标签减少显示
    plt.xticks(range(0, len(x), step), x_label[::step], rotation=45)
    # 网格显示
    plt.grid(alpha=0.4)
    plt.title(title)
    plt.legend()
    plt.show()


# 分开两张图, 比较绘制
def draw_compare_plot(x1, y1, y2, x_label, y1_label, y2_label, title, step=10):
    plt.figure(figsize=(20, 8), dpi=80)
    fig, axs = plt.subplots(2, 1)
    # 绘制数据
    axs[0].plot(range(len(x1)), y1, alpha=0.7)
    axs[1].plot(range(len(x1)), y2, alpha=0.7)
    # y轴说明
    axs[0].set_ylabel(y1_label)
    axs[1].set_ylabel(y2_label)
    # x轴标签减少显示
    plt.setp(axs, xticks=range(0, len(x1), step), xticklabels=x_label[::step])
    # x轴标签旋转
    for ax in fig.axes:
        ax.tick_params(labelrotation=45)
    # 网格显示
    axs[0].grid(alpha=0.4)
    axs[1].grid(alpha=0.4)

    fig.suptitle(title)
    plt.show()


# 绘制折线图和条形图
def draw_compare_plot_bar(x1, y1, y2, x_label, title, step=10):
    plt.figure(figsize=(20, 8), dpi=80)
    fig, axs = plt.subplots(2, 1)
    # 绘制数据
    axs[0].plot(range(len(x1)), y1, alpha=0.7)
    axs[1].bar(range(len(x1)), y2, alpha=0.7)
    # y轴说明
    axs[0].set_ylabel('stock')
    axs[1].set_ylabel('amount')
    # x轴标签减少显示
    plt.setp(axs, xticks=range(0, len(x1), step), xticklabels=x_label[::step])
    # 网格显示
    axs[0].grid(alpha=0.4)

    fig.suptitle(title)
    plt.show()


# 默认比较折线图方法
def draw_default_compare_plot(stock_df, index_df, title, step=10):
    x1 = stock_df['close'].index[::-1]
    y1 = stock_df['close'].values[::-1]
    y2 = index_df['close'].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_compare_plot(x1, y1, y2, x_label, 'stock', 'index', title, step)


def draw_default_compare_plot_bar(stock_df, title, step=10):
    x1 = stock_df['close'].index[::-1]
    y1 = stock_df['close'].values[::-1]
    y2 = stock_df['amount'].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_compare_plot_bar(x1, y1, y2, x_label, title, step)


# 绘制指定字段的比较折线图
def draw_field_compare_plot(stock_df, field, title, step=10):
    x1 = stock_df['close'].index[::-1]
    y1 = stock_df['close'].values[::-1]
    y2 = stock_df[field].values[::-1]
    x_label = stock_df['trade_date'].values[::-1]

    draw_compare_plot(x1, y1, y2, x_label, 'stock', field, title, step)


