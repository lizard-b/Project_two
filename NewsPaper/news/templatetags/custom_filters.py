from django import template
from filter_resources import censor_filter

register = template.Library()


@register.filter()
def censor(word):
    if isinstance(word, str):
        for a in word.split():
            if a.capitalize() in censor_filter:
                word = word.replace(a, a[0] + '*' * len(a))
    return word
