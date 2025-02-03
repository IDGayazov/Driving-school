from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import LessonEnrollmentForm
from .models import LessonEnrollment

def lessons_list(request):
    registrations = LessonEnrollment.objects.all()
    return render(request, 'lesson_list.html', {'registrations': registrations})

def lesson_detail(request, pk):
    lesson = get_object_or_404(LessonEnrollment, pk=pk)
    user_enrolled = False
    if request.user.is_authenticated and request.user.is_student():
        user_enrolled = lesson.student == request.user
    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'user_enrolled': user_enrolled,
    })

@login_required
def lessons_create(request):
    if request.method == 'POST':
        form = LessonEnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = LessonEnrollmentForm()
    return render(request, 'lessons_create.html', {'form': form})

@login_required
def enroll_lesson(request, lesson_id):
    lesson = get_object_or_404(LessonEnrollment, id=lesson_id)
    if request.user.is_student():
        if not lesson.student:
            lesson.student = request.user
            lesson.is_booked = True
            lesson.save()
    return redirect('lesson_list')