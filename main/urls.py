from django.urls import path
from django.contrib.auth.decorators import login_required

from main.views import home

app_name = 'main'

urlpatterns = [

    path('', home, name='home'),
]