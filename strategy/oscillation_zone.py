import pandas as pd

from common.utils.logger import Logger

log = Logger(__name__).logger


def get_oscillation_zone_df(df, field, rate=0.0155, default_period=5):
    """
    区域震荡策略
    一定周期内下降, 或者在一定比略范围内小幅度上升都会被保存
    """
    # 让数据按升序排列, 清理掉为空的数据
    df = df.dropna(axis=0, how='any')[::-1]
    period = default_period

    try:
        pre = df[field].head(1).values[0]
    except IndexError:
        log.info("Empty data.")
        return None

    result_df = pd.DataFrame()
    # 分区段走, period区间内没有符合要求数据都没有就往下走
    # 筛选连续下降的数据
    for index, row in df.iterrows():
        # 允许小幅度范围内会升
        zone_rate = abs(row[field] - pre) / pre
        if row[field] < pre or zone_rate < rate:
            period -= 1
            if period == 0:
                result_df = result_df.append(row, ignore_index=True)
                period = default_period
        else:
            # 区间往后走
            period = default_period
        pre = row[field]
    return result_df
