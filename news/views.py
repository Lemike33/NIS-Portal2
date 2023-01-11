from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from datetime import datetime
from .models import Post


class ShowNewsView(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = ['-date']  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news/showNews.html'  # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты в HTML обращаемся к нему!!!
    # paginate_by = 2  # постраничный вывод, сколько объектов выводим на 1 страницу

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_news'] = 'Ожидайте новые новости'
        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/showNewsDetail.html'
    context_object_name = 'news'


