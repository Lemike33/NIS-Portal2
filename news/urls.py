from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
   # декоратор cache_page кэширует изменения на странице news-main на 60*5=300с
   path('news/', cache_page(6*2)(views.ShowNewsView.as_view()), name='news-main'),
   path('articles/', cache_page(6*2)(views.ShowNewsView.as_view()), name='articles-main'),
   path('articles/<int:pk>', cache_page(6)(views.NewsDetailView.as_view()), name='articles-detail'),
   path('news/<int:pk>', cache_page(6)(views.NewsDetailView.as_view()), name='news-detail'),
   path('search', views.SearchNewsView.as_view(), name='news-search'),
   path('news/create', views.CreatePostsView.as_view(), name='news-create'),
   path('articles/create', views.CreatePostsView.as_view(), name='articles-create'),
   path('news/<int:pk>/update/', views.UpdatePostView.as_view(), name='news-update'),
   path('news/<int:pk>/delete/', views.DeletePost.as_view(), name='news-delete'),
   path('articles/<int:pk>/update/', views.UpdatePostView.as_view(), name='articles-update'),
   path('articles/<int:pk>/delete/', views.DeletePost.as_view(), name='articles-delete'),
]
