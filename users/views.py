from django.shortcuts import render, HttpResponseRedirect
from django.urls  import reverse, reverse_lazy
from django.views.generic.base import TemplateView

from main.models import Course, Enrollment
from users.forms import LoginForm, RegisterForm, UserProfileForm
from django.contrib import auth
from users.models import Users
from lessons.models import LessonEnrollment
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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем дополнительные данные в контекст

        user = self.request.user

        profile = Users.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile

        if profile.is_student():
            context['is_student'] = True
            course_ids = profile.enrollment_set.values_list('course', flat=True)
            
            if course_ids:
                context['course'] = Course.objects.filter(id__in=course_ids)[0]  

            practice_ids = LessonEnrollment.objects.select_related('student').filter(student=profile)

            if practice_ids:
                print(LessonEnrollment.objects.filter(id__in=practice_ids))
                context['practices'] = LessonEnrollment.objects.filter(id__in=practice_ids)
        
        elif profile.is_teacher():
            context['is_teacher'] = True

            courses_with_students = {}

            courses = Course.objects.filter(created_by=profile)
            
            for course in courses:
                enrollments = Enrollment.objects.select_related('student').filter(course=course)
                students = [enrollment.student for enrollment in enrollments]
                courses_with_students[course] = students

            context['courses_with_students'] = courses_with_students
        
        elif profile.is_instructor():
            enrollments = LessonEnrollment.objects.select_related('student').filter(instructor=profile)
            students = [enrollment.student for enrollment in enrollments]
            context['is_instructor'] = True
            context['students'] = students
        
        elif profile.is_admin():
            context['is_admin'] = True

        return context


class UserProfileEditView(UpdateView):
    model = Users
    form_class = UserProfileForm
    template_name = 'users/edit-profile.html'
    title = 'Редактироавние профиля'

    def get_success_url(self):
        # Возвращаем URL профиля текущего пользователя
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})
