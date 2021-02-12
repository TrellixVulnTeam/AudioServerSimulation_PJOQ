from datetime import datetime


def is_positive(number: int):
    if number <= 0:
        return False
    return True


def future_date(date: str):
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if date <= datetime.now():
        return False
    return True