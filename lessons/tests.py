from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Users
from .models import LessonEnrollment
from .views import lessons_list, lessons_create, enroll_lesson, cancel_enrollment, delete_lesson
from .forms import LessonEnrollmentForm
from datetime import date, timedelta
from django.core.exceptions import ValidationError



class LessonsViewsTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя (администратора)
        self.admin_user = Users.objects.create_user(
            username='admin',
            password='adminpassword',
            role='admin'
        )

        # Создаем тестового пользователя (инструктора)
        self.instructor_user = Users.objects.create_user(
            username='instructor',
            password='instructorpassword',
            role='instructor'
        )

        # Создаем тестового пользователя (студента)
        self.student_user = Users.objects.create_user(
            username='student',
            password='studentpassword',
            role='student'
        )

        # Создаем тестовое занятие
        self.lesson = LessonEnrollment.objects.create(
            date='2023-12-01',
            instructor=self.instructor_user,  # Используем self.instructor_user
            car_brand='Toyota',
            car_number='A123BC45'
        )

        # Инициализация клиента для тестирования
        self.client = Client()

    def test_lessons_list_view(self):
        # Проверка доступа к списку занятий
        response = self.client.get(reverse('lessons:lessons_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons_list.html')

    def test_lessons_create_view_get(self):
        # Проверка доступа к форме создания занятия для инструктора
        self.client.force_login(self.instructor_user)
        response = self.client.get(reverse('lessons:lessons_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons_create.html')

    def test_lessons_create_view_post(self):
        # Проверка создания занятия инструктором
        self.client.force_login(self.instructor_user)
        data = {
            'date': '2026-12-02',
            'instructor': self.instructor_user.id,
            'car_brand': 'Honda',
            'car_number': 'А456СЕ78'
        }
        response = self.client.post(reverse('lessons:lessons_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LessonEnrollment.objects.filter(car_brand='Honda').exists())

    def test_enroll_lesson_view(self):
        # Проверка записи студента на занятие
        self.client.force_login(self.student_user)
        response = self.client.post(reverse('lessons:enroll_lesson', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 302)  # Редирект после успешной записи
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.student, self.student_user)
        self.assertTrue(self.lesson.is_booked)

    def test_cancel_enrollment_view(self):
        # Проверка отмены записи студента на занятие
        self.lesson.student = self.student_user
        self.lesson.is_booked = True
        self.lesson.save()

        self.client.force_login(self.student_user)
        response = self.client.post(reverse('lessons:cancel_enrollment', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 302)  # Редирект после успешной отмены
        self.lesson.refresh_from_db()
        self.assertIsNone(self.lesson.student)
        self.assertFalse(self.lesson.is_booked)

    def test_delete_lesson_view_admin(self):
        # Проверка удаления занятия администратором
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('lessons:delete_lesson', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertFalse(LessonEnrollment.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_view_instructor(self):
        # Проверка удаления занятия инструктором (если он создал занятие)
        self.client.force_login(self.instructor_user)
        response = self.client.post(reverse('lessons:delete_lesson', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertFalse(LessonEnrollment.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_view_instructor_denied(self):
        # Проверка запрета удаления занятия, если инструктор не создал его
        another_instructor = Users.objects.create_user(
            username='another_instructor',
            password='anotherpassword',
            role='instructor'
        )
        self.client.force_login(another_instructor)
        response = self.client.post(reverse('lessons:delete_lesson', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'error': 'У вас нет прав на удаление этого занятия.'})
        self.assertTrue(LessonEnrollment.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_view_student_denied(self):
        # Проверка запрета удаления занятия студентом
        self.client.force_login(self.student_user)
        response = self.client.post(reverse('lessons:delete_lesson', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'error': 'У вас нет прав на удаление этого занятия.'})
        self.assertTrue(LessonEnrollment.objects.filter(id=self.lesson.id).exists())

    def test_invalid_car_number(self):
        """Тест: Невалидный номер машины"""
        lesson = LessonEnrollment(
            car_number= "555555",
            instructor=self.instructor_user,

        )
        with self.assertRaises(ValidationError) as context:
            lesson.full_clean()
