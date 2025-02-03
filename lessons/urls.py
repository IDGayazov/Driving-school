from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons_list, name='lesson_list'),
    path('create/', views.lessons_create, name='lesson_create'),
    path('lesson/<int:lesson_id>/enroll/', views.enroll_lesson, name='enroll_lesson'),
]