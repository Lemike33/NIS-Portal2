from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group
from .models import BaseRegisterForm

# def register(request):
#     if request.method == "POST":
#         form = UserOurRegistration(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             return redirect('user-input')
#     else:
#         form = UserOurRegistration()
#     return render(request, 'users/registration.html', {'form': form, 'title': 'Регистрация пользователя'})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='common')
    if not request.user.groups.filter(name='common').exists():
        premium_group.user_set.add(user)
    return redirect('/users')
