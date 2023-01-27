from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery import shared_task
from datetime import datetime, timedelta
from .models import Post


@shared_task
def sending_posts_on_schedule():
    current_date = datetime.today()  # вычисляем сегодняшнюю дату
    week_ago_date = current_date - timedelta(days=7)
    name_letter = 'Посты за неделю!'
    #  делаем выборку постов за прошедшие 7 дней - методом filter
    posts_set = Post.objects.filter(date__range=(week_ago_date, current_date)).order_by('-date')

    for post in posts_set:
        if posts_set.count() == 0:
            continue
        else:
            html_content = render_to_string(
                'news/message_created.html',
                {
                    'title': post.title,
                    'text': post.text,
                    'author': post.author,
                }
            )

            msg = EmailMultiAlternatives(
                subject=name_letter,
                body=f'посты за неделю',  # это то же, что и message
                from_email='lemikes33@yandex.ru',
                to=['leshukovv87@mail.ru'],  # это то же, что и recipients_list
                )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем письмо




