from django.http import HttpResponse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime
from .models import Post, CategoryUser
from .filters import NewsFilter
from .forms import NewsForm


class ShowNewsView(ListView):
    """List of all posts with pagination."""
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = ['-date']  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news/showNews.html'  # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты в HTML обращаемся к нему!!!
    paginate_by = 10  # постраничный вывод, сколько объектов выводим на 1 страницу

    # Метод get_context_data позволяет нам изменить набор данных(например добавить новые time_now, next_news),
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

    # переопределяем функцию получения набра данных из модели
    def get_queryset(self):
        if 'news' in self.request.path:
            self.queryset = super().get_queryset().filter(select='N')
            return self.queryset
        else:
            self.queryset = super().get_queryset().filter(select='P')
            return self.queryset


class SearchNewsView(ListView):
    """Search for posts by selected filters."""
    model = Post
    template_name = 'news/searchNews.html'
    context_object_name = 'news'
    paginate_by = 3

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
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
    """Displaying detailed information for each post."""
    model = Post
    template_name = 'news/showNewsDetail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # находим категорию текущего поста
        post_cat = Post.objects.get(pk=self.kwargs['pk']).categories.values('category_name').get()
        context['post_cat'] = post_cat.get('category_name')

        # определяем текущего пользователя
        auth_user = self.request.user
        context['auth_user'] = auth_user

        return context


class CreatePostsView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """ класс для создания веб-сервиса для добавления постов(новостей/статей) """
    model = Post
    template_name = "news/create_post.html"
    form_class = NewsForm
    permission_required = ('news.add_post', 'news.change_post')

    def form_valid(self, form):
        """Select event type post or news."""
        post = form.save(commit=False)
        # если путь такой: http://127.0.0.1:8000/posts/news/create то выбираем, что это новость
        if 'news' in self.request.path.split('/'):
            post.select = 'N'
            post.save()
        else:
            post.select = 'P'
            post.save()
        return super().form_valid(form)

    def get_absolute_url(self):
        if 'news' in self.request.path:
            return reverse('news-detail', args=[str(self.id)])
        elif 'articles' in self.request.path:
            return reverse('articles-detail', args=[str(self.id)])
        else:
            pass

    #  метод для отправки созданной статьи пользователю
    def post(self, request, *args, **kwargs):
        """Method to send created article to user."""
        if request.method == "POST":
            message = NewsForm(request.POST)
            if message.is_valid():
                message.save()

                title = request.POST['title']
                text = request.POST['text']
                author = request.POST['author']
                send_to = ["leshukovv87@mail.ru"]
                link = self.request.path

                # получаем наш html
                html_content = render_to_string(
                    'news/message_created.html',
                    {
                        'title': title,
                        'text': text,
                        'author': author,
                        'link': link,

                    }
                )

                msg = EmailMultiAlternatives(
                    subject=title,
                    body=text,
                    from_email='lemikes33@yandex.ru',
                    to=['leshukovv87@mail.ru'],
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html

                msg.send()

        return redirect('/users')


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "news/create_post.html"
    form_class = NewsForm
    success_url = reverse_lazy('news-main')

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    #  url куда переправлять пользователя после успешного удаления товара.
    success_url = reverse_lazy('news-main')


class AddFavoriteCategory(LoginRequiredMixin, TemplateView):
    model = CategoryUser
    template_name = 'news/showNewsDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        return context

    def test(self):
        self.cats = self.CategoryUser.objects.filter(user=1)
        for cat in self.cats:
            print(cat)
















