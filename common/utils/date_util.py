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


if __name__ == '__main__':
    print(get_last_bus_day())
