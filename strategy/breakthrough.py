import pandas as pd


def get_fall_down_df(df, field, default_period=5):
    """
    下降突破策略
    """
    # 让数据按升序排列, 清理掉为空的数据
    df = df.dropna(axis=0, how='any')[::-1]
    period = default_period

    try:
        pre = df[field].head(1).values[0]
    except IndexError:
        print("Empty data.")
        return None

    result_df = pd.DataFrame()
    # 分区段走, period区间内没有符合要求数据都没有就往下走
    # 筛选连续下降的数据
    for index, row in df.iterrows():
        # 允许小幅度范围内会升
        zone_rate = abs(row[field] - pre) / pre
        if row[field] < pre or zone_rate < 0.0155:
            period -= 1
            if period == 0:
                result_df = result_df.append(row, ignore_index=True)
                period = default_period
        else:
            # 区间往后走
            period = default_period
        pre = row[field]
    return result_df
