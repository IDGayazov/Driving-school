from django.shortcuts import render, HttpResponseRedirect
from django.urls  import reverse, reverse_lazy
from django.views.generic.base import TemplateView

from users.forms import LoginForm, RegisterForm, UserProfileForm
from django.contrib import auth
from users.models import Users
from django.contrib.auth.views import LoginView

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView

class UserLoginForm(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    title = 'Вход'

    def get_success_url(self):
        # Возвращаем URL профиля текущего пользователя
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})



class UserRegistrationView(CreateView):
    model = Users
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Регистрация'


class UserProfileView(DetailView):
    model = Users
    template_name = 'users/profile.html'
    title = 'Профиль'


class UserProfileEditView(UpdateView):
    model = Users
    form_class = UserProfileForm
    template_name = 'users/edit-profile.html'
    title = 'Редактироавние профиля'

    def get_success_url(self):
        # Возвращаем URL профиля текущего пользователя
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})
