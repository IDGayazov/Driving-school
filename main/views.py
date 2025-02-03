from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    
    if request.method == 'POST':
        Enrollment.objects.create(course=course, student=request.user)
        course.places_count -= 1
        course.save()
        return redirect('main:home')

    return render(request, 'main/main.html')

@login_required
def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    
    courses = Course.objects.filter(category=category)
    
    enrolled = Enrollment.objects.filter(student=request.user).values_list('course', flat=True)
    print(enrolled)

    return render(request, 'main/category_detail.html', {
        'category': category,
        'courses': courses,
        'enrolled': enrolled,
    })