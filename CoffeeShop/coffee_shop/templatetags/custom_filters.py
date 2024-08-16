from django import template
# from filter_res import CURRENCIES_SYMBOLS

register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': '₽',
   'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'
