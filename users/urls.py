from django.urls import path
from django.contrib.auth.decorators import login_required

from users.views import UserLoginForm, UserProfileEditView, UserRegistrationView, UserProfileView
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [

    path('login/', UserLoginForm.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('profile/<int:pk>/edit_profile', login_required(UserProfileEditView.as_view()), name='edit_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]