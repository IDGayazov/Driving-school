from django.shortcuts import render, HttpResponseRedirect
from django.urls  import reverse, reverse_lazy
from django.views.generic.base import TemplateView

from users.forms import LoginForm, RegisterForm, UserProfileForm
from django.contrib import auth
from users.models import Users
from django.contrib.auth.views import LoginView

from django.views.generic.edit import CreateView, UpdateView


class UserLoginForm(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    title = 'Вход'



class UserRegistrationView(CreateView):
    model = Users
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Регистрация'


class UserProfileView(UpdateView):
    model = Users
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Профиль'
