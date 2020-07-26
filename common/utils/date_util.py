from datetime import datetime
from datetime import timedelta
import time

DATE_FORMATTER = '%Y%m%d'


# 结束日期为当天
def get_now_date():
    return datetime.now().strftime(DATE_FORMATTER)


# 某个日期几天前的时间
def get_days_ago(days):
    days_ago = datetime.now() - timedelta(days=days)
    return time.strftime(DATE_FORMATTER, days_ago.timetuple())


if __name__ == '__main__':
    print(get_days_ago(6))
