from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django import forms

from users.models import Users
import uuid
from datetime import timedelta
from django.utils.timezone import now


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите логин'
    }),)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль'
    }),)

    class Meta:
        model = Users
        fields = ('username', 'password')


# n@3gPhFF=pyZYSe
class RegisterForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя'
    }), max_length=100)

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите фамилию'
    }),max_length=100)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите логин'
    }),max_length=100)

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите номер телефона'
    }),max_length=100)

    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите почту'
    }),max_length=100)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль'
    }), max_length=100)

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Повторите пароль'
    }),  max_length=100)

    class Meta:
        model = Users
        fields = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        # Отключаем валидацию email
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=True)
        user.is_active = True 
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 mb-4 bg-gray-200 text-black  border-b border-gray-600 focus:outline-none focus:border-blue-500',
        'placeholder': 'Введите Имя'
    }),)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 mb-4 bg-gray-200 text-black  border-b border-gray-600 focus:outline-none focus:border-blue-500',
        'placeholder': 'Введите логин',
        'readonly': True
    }),)
    
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 mb-4 bg-gray-200 text-black  border-b border-gray-600 focus:outline-none focus:border-blue-500',
        'placeholder': 'Введите почту',
        'readonly': True
    }),)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'w-full p-2 mb-4 bg-gray-200 text-black  border-b border-gray-600 focus:outline-none focus:border-blue-500',
        'placeholder': 'Фотка',
    }))

    class Meta:
        model = Users
        fields = ('first_name', 'username', 'email', 'image')