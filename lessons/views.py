from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from users.models import Users
from .forms import LessonEnrollmentForm
from .models import LessonEnrollment
import logging

logger = logging.getLogger(__name__)

def lessons_list(request):
    registrations = LessonEnrollment.objects.all()

    sort_by = request.GET.get('sort_by', 'date_asc')
    if sort_by == 'date_asc':
        registrations = registrations.order_by('date')
    elif sort_by == 'date_desc':
        registrations = registrations.order_by('-date')

    filter_by = request.GET.get('filter_by')
    if filter_by == 'booked':
        registrations = registrations.filter(is_booked=True)
    elif filter_by == 'available':
        registrations = registrations.filter(is_booked=False)

    return render(request, 'lessons/lessons_list.html', {
        'registrations': registrations,
        'sort_by': sort_by,
        'filter_by': filter_by,
    })

@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(LessonEnrollment, pk=pk)
    user_enrolled = False
    if request.user.is_authenticated and request.user.is_student():
        user_enrolled = lesson.student == request.user
    instructor = get_object_or_404(Users, pk=lesson.instructor_id)
    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'user_enrolled': user_enrolled,
        'instructor': instructor.get_full_name()  # Исправлено: instructor и get_full_name()
    })

@login_required
def lessons_create(request):
    if request.user.is_student():
        raise PermissionDenied

    if request.method == 'POST':
        form = LessonEnrollmentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lessons:lessons_list')
    else:
        form = LessonEnrollmentForm(user=request.user)

    return render(request, 'lessons/lessons_create.html', {'form': form})

@login_required
def enroll_lesson(request, lesson_id):
    lesson = get_object_or_404(LessonEnrollment, id=lesson_id)
    if request.user.is_student():
        if not lesson.student:
            lesson.student = request.user
            lesson.is_booked = True
            lesson.save()
    return redirect('lessons/lessons_list')