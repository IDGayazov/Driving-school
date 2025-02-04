from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lessons_list, name='lessons_list'),
    path('create/', views.lessons_create, name='lessons_create'),
    path('lesson/<int:lesson_id>/enroll/', views.enroll_lesson, name='enroll_lesson'),
]