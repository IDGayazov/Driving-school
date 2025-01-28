from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import EnrollmentForm
from .models import Course, Enrollment

from main.models import Category

def home(request):
    context = {
        "categories_list": Category.objects.get_queryset()
    }
    return render(request, 'main/main.html', context)

@login_required
def enroll_in_course(request, course_id):
    course = Course.objects.get(id=course_id)

    # Проверяем, что курс не переполнен
    if Enrollment.objects.filter(course=course).count() >= course.max_students:
        return HttpResponse('Курс переполнен', status=400)

    # Если пользователь уже записан на этот курс
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        return HttpResponse('Вы уже записаны на этот курс', status=400)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, user=request.user)
        if form.is_valid():
            # Записываем студента на курс
            form.instance.student = request.user
            form.save()
            return redirect('course_list')  # Перенаправление на страницу с курсами
    else:
        form = EnrollmentForm(user=request.user)

    return render(request, 'enroll_in_course.html', {'form': form, 'course': course})

@login_required
def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    
    courses = Course.objects.filter(category=category)
    
    # Проверяем, записан ли пользователь на этот курс
    enrolled = False
    
    return render(request, 'main/category_detail.html', {
        'category': category,
        'courses': courses,
        'enrolled': enrolled,
    })