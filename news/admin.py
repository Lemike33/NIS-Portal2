from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory, CategoryUser


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Displaying the model in the admin panel."""
    list_display = ('user', 'rating_author')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'select', 'date', 'rating_post')
    list_filter = ('author', 'date', 'rating_post')
    fields = ['author', 'date', ('select', 'rating_post')]
    list_display_links = ('rating_post', 'author', 'date')
    search_fields = ('categories',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('date_created', 'post', 'user')


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')


@admin.register(CategoryUser)
class CategoryUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')


