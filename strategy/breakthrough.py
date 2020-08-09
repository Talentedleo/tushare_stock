def get_fall_down_dict(df, field, default_period=5):
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

    record = {}
    # 分区段走, period区间内没有符合要求数据都没有就往下走
    # 筛选连续下降的数据
    for index, row in df.iterrows():
        if row[field] < pre:
            period -= 1
            if period == 0:
                record[index] = row
                period = default_period
        else:
            # 区间往后走
            period = default_period
        pre = row[field]
    return record
