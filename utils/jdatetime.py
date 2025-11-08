# Third Party Packages
from jdatetime import datetime as jalali_datetime
from datetime import datetime


def convert_to_jalali(instance):
    """تبدیل تاریخ میلادی به جلالی"""
    return jalali_datetime.fromgregorian(datetime=instance)


def standard_jalali_datetime_format(instance):
    """فرمت استاندارد تاریخ و ساعت جلالی"""
    return convert_to_jalali(instance).strftime('%H:%M %Y/%m/%d')


def standard_jalali_date_format(instance):
    """فرمت استاندارد فقط تاریخ جلالی"""
    return convert_to_jalali(instance).strftime('%Y/%m/%d')


def pretty_jalali_datetime_format(instance):
    """فرمت تاریخ جلالی به‌صورت زیبا (مثلاً ۲۳ مهر ۱۴۰۳)"""
    _instance = convert_to_jalali(instance)
    months = (
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    )
    return _instance.strftime('%d {} %Y'.format(months[int(_instance.strftime('%m')) - 1]))


def humanize_datetime(instance):
    """
    تبدیل زمان به عبارت قابل‌خواندن برای انسان
    مثال: چند لحظه قبل، یک ساعت قبل، دیروز، ...
    """
    if isinstance(instance, datetime):
        difference = datetime.now() - instance.replace(tzinfo=None)
    else:
        raise ValueError('ورودی باید از نوع datetime باشد.')

    days_past = difference.days
    seconds_past = difference.seconds

    if days_past == 0:
        if seconds_past < 10:
            return 'چند لحظه قبل'
        if seconds_past < 60:
            return f'{int(seconds_past)} ثانیه قبل'
        if seconds_past < 120:
            return 'یک دقیقه قبل'
        if seconds_past < 3600:
            return f'{int(seconds_past / 60)} دقیقه قبل'
        if seconds_past < 7200:
            return 'یک ساعت قبل'
        if seconds_past < 86400:
            return f'{int(seconds_past / 3600)} ساعت قبل'
    if days_past == 1:
        return 'دیروز'
    if days_past < 7:
        return f'{int(days_past)} روز قبل'
    if days_past < 31:
        return f'{int(days_past / 7)} هفته قبل'
    if days_past < 365:
        return f'{int(days_past / 30)} ماه قبل'
    return f'{int(days_past / 365)} سال قبل'
