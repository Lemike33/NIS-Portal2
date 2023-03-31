from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from .resourses import SELECT
from django.urls import reverse
from django.utils.translation import gettext as _


class Author(models.Model):
    """Template for all objects of type author."""
    user = models.OneToOneField(User, verbose_name='Автор', on_delete=models.CASCADE)  # при удалении пользователя удаляться и все его статьи
    rating_author = models.IntegerField(default=0, verbose_name='Рейтинг автора')

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
    """Template for all objects of type category."""
    category_name = models.CharField(unique=True, max_length=50, verbose_name='Уникальная тема', help_text=_('category names!'))
    subscribers = models.ManyToManyField(User, through='CategoryUser')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    """Contains articles and news created by users."""
    post = 'P'
    news = 'N'

    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE, related_name='posts')
    select = models.CharField('Статья или Новость', max_length=10, choices=SELECT, default=post)
    date = models.DateTimeField('Дата', default=timezone.now)
    categories = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория:')
    title = models.CharField('Название статьи', max_length=120, unique=True)
    text = models.TextField('Основной текст статьи')
    rating_post = models.IntegerField(default=0, verbose_name='Рейтинг:')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date']  # сортировка с конца списка articles

    def like(self):
        """Like increment method."""
        self.rating_post += 1
        self.save()
        return self.rating_post

    def dislike(self):
        """Like decriment method."""
        if self.rating_post != 0:
            self.rating_post -= 1
            self.save()
        return self.rating_post

    def preview(self):
        """First 120 character preview method."""
        if len(str(self.text)) <= 120:
            return self.text
        else:
            return self.text[:120] + ' ... '

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        """Method that returns a unique reference to an object."""
        return reverse('news-detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    """Intermediate model for many-to-many relationships."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Имя поста:{self.post} - Имя категории:{self.category}'


class Comment(models.Model):
    """Template for all objects of type comment."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_posts')  # many to many
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
    """Intermediate model for many-to-many relationships."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.user} - {self.category}'










