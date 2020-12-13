import time
from datetime import datetime, date
from datetime import timedelta

DATE_FORMATTER = '%Y%m%d'


# 结束日期为当天
def get_now_date():
    return datetime.now().strftime(DATE_FORMATTER)


# 某个日期几天前的时间
def get_days_ago(days):
    days_ago = datetime.now() - timedelta(days=days)
    return time.strftime(DATE_FORMATTER, days_ago.timetuple())


# 获取最近一个工作日
def get_last_bus_day():
    last_bus_day = datetime.now()
    if date.weekday(last_bus_day) == 5:
        # if it's Saturday then make it Friday
        last_bus_day = last_bus_day - timedelta(days=1)
    elif date.weekday(last_bus_day) == 6:
        # if it's Sunday then make it Friday
        last_bus_day = last_bus_day - timedelta(days=2)
    return last_bus_day.strftime(DATE_FORMATTER)


# 获取季度数据 start_q='2018Q1', end_q='2019Q3'
def get_quarter_date():
    today = date.today()
    quarter = (today.month - 1) // 3 + 1
    return '{}Q{}'.format(today.year, quarter)


# n天前的季度
def get_quarter_date_ago(days=30):
    before_day = datetime.now() - timedelta(days=days)
    quarter = (before_day.month - 1) // 3 + 1
    return '{}Q{}'.format(before_day.year, quarter)


# 字符串日期获取n天前的日期字符串
def transform_str_date_ago(date_str, days):
    date_time = datetime.strptime(date_str, DATE_FORMATTER)
    days_ago = date_time - timedelta(days=days)
    return time.strftime(DATE_FORMATTER, days_ago.timetuple())


# 字符串日期获取n天后的日期字符串
def transform_str_date_after(date_str, days):
    date_time = datetime.strptime(date_str, DATE_FORMATTER)
    days_after = date_time + timedelta(days=days)
    return time.strftime(DATE_FORMATTER, days_after.timetuple())


if __name__ == '__main__':
    get_quarter_date_ago()

    after = transform_str_date_after('20201130', 3)
    print(after)
