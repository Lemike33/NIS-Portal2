from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory, CategoryUser

MODELS = [Author, Category, Post, Comment, PostCategory, CategoryUser]
for model in MODELS:
    admin.site.register(model)

