from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewsForm(forms.ModelForm):
    """Create a form for writing a post/news model object to the database (POST method)."""
    class Meta:
        model = Post
        #  поле select(новость/статья) не указываю, так как оно определяется во views через метод form_valid
        #  там в зависимости от url ссылки подставляем в него Р - если пост, N - если статья!
        fields = [
            'author',
            'categories',
            'title',
            'text',
            'rating_post',
        ]

    # позволяет делать свои проверки на валидность полей таблицы
    def clean(self):
        """Make your own checks for the validity of table fields."""
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
