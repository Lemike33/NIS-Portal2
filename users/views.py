from django.shortcuts import render, redirect
from .forms import UserOurRegistration
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == "POST":
        form = UserOurRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('user-input')
    else:
        form = UserOurRegistration()
    return render(request, 'users/registration.html', {'form': form, 'title': 'Регистрация пользователя'})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

