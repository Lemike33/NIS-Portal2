from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils import timezone
from .resourses import SELECT, post, news
from django.urls import reverse


class Author(models.Model):
    """Model including objects of all authors"""
    user = models.OneToOneField(User, verbose_name='Автор', on_delete=models.CASCADE)  # при удалении пользователя удаляться и все его статьи
    rating_author = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3
        # posts - это связанное поле из класса Post полученное через related_name поля author модели Post

        sum_rating_post = self.posts.aggregate(result=Sum('rating_post')).get('result')

        # суммарный рейтинг всех комментариев автора
        author_comments = self.user.comments_users.filter(user_id=self.user)
        count_comment = 0
        for com in author_comments:
            count_comment += com.rating_comment

        # суммарный рейтинг всех чужих комментариев к статьям автора

        self.rating_author = sum_rating_post * 3 + count_comment
        self.save()
        return self.rating_author

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    """Themes of news"""
    category_name = models.CharField(unique=True, max_length=50, verbose_name='Уникальная тема')
    subscribers = models.ManyToManyField(User, through='CategoryUser')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    """Contains articles and news created by users"""
    post = 'P'
    news = 'N'

    # related_name='posts' - для связи с моделью Author, что бы можно было из модели Author видеть посты этого автора
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE, related_name='posts')
    select = models.CharField('Статья/Новость', max_length=10, choices=SELECT, default=post)
    date = models.DateTimeField('Дата', default=timezone.now)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField('Название статьи', max_length=120, unique=True)
    text = models.TextField('Основной текст статьи')
    rating_post = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def like(self):
        self.rating_post += 1
        self.save()
        return self.rating_post

    def dislike(self):
        if self.rating_post != 0:
            self.rating_post -= 1
            self.save()
        return self.rating_post

    def preview(self):
        if len(str(self.text)) <= 120:
            return self.text
        else:
            return self.text[:120] + ' ... '

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    """Intermediate model for many-to-many relationships"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Имя поста:{self.post} - Имя каткгории:{self.category}'


class Comment(models.Model):
    """Comment storage model"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_posts')  # связь один ко многим
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_users')
    text = models.TextField('Основной текст комментария')
    date_created = models.DateTimeField('Дата', default=timezone.now)
    rating_comment = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.rating_comment += 1
        self.save()
        return self.rating_comment

    def dislike(self):
        if self.rating_comment != 0:
            self.rating_comment -= 1
            self.save()
        return self.rating_comment

    def __str__(self):
        return f'Комментарий к посту: -  "{self.post}" от автора: - "{self.user}"'


class CategoryUser(models.Model):
    """ Класс для связи многие-ко-многим категории/пользователи """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.category}'










