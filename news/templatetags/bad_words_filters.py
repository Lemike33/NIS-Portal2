"""
Описание:

"""
import re
from django import template
from ..resourses import BAD
register = template.Library()


@register.filter()
def bad_words(value):
    text_list = re.split(r'[,;!).? ]+', value)
    clean_list = []
    for el in text_list:
        if (el.lower() or el.title()) in BAD:
            el = el[0] + ((len(el) - 1) * '*')
            clean_list.append(el)
        else:
            clean_list.append(el)
    clean_text = " ".join(clean_list)
    value = clean_text
    return f'{value}'









