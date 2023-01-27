# 6 --В первую очередь мы импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery.

# 7 --Второй строчкой мы связываем настройки Django с настройками Celery через переменную окружения.

# 9-12 --Далее мы создаём экземпляр приложения Celery и устанавливаем для него файл конфигурации.
# Мы также указываем пространство имён, чтобы Celery сам находил все необходимые настройки
# в общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***».

# 14 --Последней строчкой мы указываем Celery автоматически искать задания в файлах
# tasks.py каждого приложения проекта.

# crontab Examples:
# crontab()   Каждая минута
# crontab(minute=0, hour=0)   Ежедневно в полночь
# crontab(minute=0, hour='*/3')	Каждые три часа: 00:00, 03:00, 06:00, 09:00 и т. д.
# crontab(minute=0, hour='0,3,6,9,12,15,18,21')	То же самое
# crontab(minute='*/15')	Выполнять каждые 15 минут
# crontab(day_of_week='sunday')	Выполнять каждую минуту (!) в воскресенье
# crontab(minute='*', hour='*', day_of_week='sun')	Аналогично предыдущему
# crontab(minute=0, hour='*/2,*/3')	Выполнять каждый чётный час и каждый час, который делится на 3
# crontab(0, 0, day_of_month='2')	Выполнять во второй день каждого месяца
# crontab(0, 0, day_of_month='2-30/2')	Выполнять каждый чётный день
# crontab(0, 0, day_of_month='11',month_of_year='5')	Выполнять только 11 мая каждого года


import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infoPortal.settings')

app = Celery('infoPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


#  словарь app.conf.beat_schedule для хранения объектов задач по расписанию
#  сейчас одна задача sending_posts_on_schedule смотри news/tasks.py
app.conf.beat_schedule = {
    'sending_out_the_latest_posts': {
        'task': 'news.tasks.sending_posts_on_schedule',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),  # выполняется по расписанию каждый понедельник в 8:00
        'args': (),
    },
}