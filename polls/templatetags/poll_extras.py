from django import template
from jalali_date import date2jalali, datetime2jalali

register = template.Library()


@register.filter(name='date')
def show_jalali_date(value):
    return date2jalali(value)


@register.filter(name='datetime')
def show_jalali_datetime(value):
    return datetime2jalali(value)


@register.filter(name='three_digit_count')
def three_digits(value):
    return '{:,}'.format(value) + ' تومان '


@register.simple_tag
def multiply(count, price):
    return three_digits(count * price)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def plus(prices):
    total_price = sum(prices)
    return three_digits(total_price)


@register.simple_tag
def total(price):
    if isinstance(price, list):
        total_price = sum(price)
        return three_digits(total_price)
    return "0"
