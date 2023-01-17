from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name='users/user.html'), name='user-input'),
    path('exit', LogoutView.as_view(template_name='users/exit.html'), name='user-exit'),
    path('reg/', views.BaseRegisterView.as_view(template_name='users/registration.html'), name='reg'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('upgrade/', views.upgrade_me, name='upgrade')
]