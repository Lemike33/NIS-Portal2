from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

MODELS = [Author, Category, Post, Comment, PostCategory]
for model in MODELS:
    admin.site.register(model)

