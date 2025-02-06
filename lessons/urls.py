from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lessons_list, name='lessons_list'),
    path('create/', views.lessons_create, name='lessons_create'),
    path('enrollLesson/<int:lesson_id>/', views.enroll_lesson, name='enroll_lesson'),
    path('cancelEnrollment/<int:lesson_id>/', views.cancel_enrollment, name='cancel_enrollment'),  # Новый маршрут
]