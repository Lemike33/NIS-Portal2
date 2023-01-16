
from django import forms
from django_filters import *
from .models import Post
from .resourses import SELECT

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
# class NewsFilter(FilterSet):


class NewsFilter(FilterSet):
    """ """

    # это поле date, оно тоже выведется в форму, использую виджет DateTime с атрибутами, type=date -
    # создает поле типа <input type='date' - выводит календарь
    date = DateFilter(field_name='date',
                      widget=forms.DateInput(attrs={'class': 'form', 'type': 'date'}),
                      lookup_expr='gt', label='Показать новости после:'
                      )
    title = CharFilter(lookup_expr='icontains')

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # из которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели ведем фильтрацию
        fields = ['select']
