from django import template

register = template.Library()
CURRENCIES_SYMBOLS = {
   'score': 'баллов',

}

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value, code):
    """ value: значение, к которому нужно применить фильтр """

    #  Возвращаемое функцией значение подставится в шаблон.
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'
