import logging
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse
from django.urls import reverse_lazy

from datetime import datetime
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm


logger = logging.getLogger(__name__)


class ShowNewsView(ListView):
    """ """
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = ['-date']  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news/showNews.html'  # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты в HTML обращаемся к нему!!!
    paginate_by = 4  # постраничный вывод, сколько объектов выводим на 1 страницу

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
        # чтобы на её примере рассмотреть работу ещё одного фильтра
        # next_news|default_if_none:"Чуть позже появятся новые новости!
        context['next_news'] = 'Ожидайте новые новости'
        return context

    def get_queryset(self):
        if 'news' in self.request.path:
            self.queryset = super().get_queryset().filter(select='N')
            return self.queryset
        else:
            self.queryset = super().get_queryset().filter(select='P')
            return self.queryset


class SearchNewsView(ListView):
    """ Класс для поиска новостей по фильтрам """
    model = Post
    template_name = 'news/searchNews.html'
    context_object_name = 'news'
    paginate_by = 2

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/showNewsDetail.html'
    context_object_name = 'news'


class CreatePostsView(CreateView):
    """ класс для создания веб-сервиса для добавления постов(новостей/статей) """
    model = Post
    template_name = "news/create_post.html"
    form_class = NewsForm

    def form_valid(self, form):
        """ Определяем чем является пост новостью или статьей в зависимости от пути страницы с которой он вызывается"""
        post = form.save(commit=False)
        # если путь такой: http://127.0.0.1:8000/posts/news/create то выбираем, что это новость
        if 'news' in self.request.path:
            post.select = 'N'
            return super().form_valid(form)
        else:
            post.select = 'P'
            return super().form_valid(form)

    def get_absolute_url(self):
        if 'news' in self.request.path:
            return reverse('news-detail', args=[str(self.id)])
        elif 'articles' in self.request.path:
            return reverse('articles-detail', args=[str(self.id)])
        else:
            pass


class UpdatePostView(UpdateView):
    model = Post
    template_name = "news/create_post.html"
    form_class = NewsForm

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])


class DeletePost(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news-main')









