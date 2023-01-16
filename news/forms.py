from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    """ создаем форму для записи обьекта модели в БД (POST-метод)"""
    class Meta:
        model = Post
        #  поле select(новость/статья) не указываю, так как оно определяется во views через метод form_valid
        #  там в зависимости от url ссылки подставляем в него Р - если пост, N - если статья!
        fields = [
            'author',
            'title',
            'text',
            'rating_post',
        ]

    # позволяет делать свои проверки на валидность полей таблицы
    def clean(self):
        cleaned_data = super().clean()
        #  получаем значение поля "text"
        text = cleaned_data.get("text")
        #  получаем значение поля "title"
        title = cleaned_data.get("title")
        #  Сравниваем их, если они равны выбрасываем исключение
        if title == text:
            raise ValidationError(
                "Название статьи не равно ее содержимому!"
            )

        return cleaned_data
