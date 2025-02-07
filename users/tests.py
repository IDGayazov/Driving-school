from datetime import datetime, timezone
from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from main.models import Category, Course, Enrollment
from users.models import Users

class UserLoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create_user(username='testuser', password='password')

    def test_user_login_page(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'password'})
        self.assertRedirects(response, reverse('users:profile', kwargs={'pk': self.user.pk}))


class UserProfileEditViewTestCase(TestCase):

    def setUp(self):
        self.user = Users.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_edit_profile_page(self):
        response = self.client.get(reverse('users:edit_profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit-profile.html')

class UserProfileViewTeacherTestCase(TestCase):

    def setUp(self):
        self.user = Users.objects.create_user(username='testteacher', password='password')
        self.category = Category.objects.create(name='A', title="adasd", description='sdfsdf')
        self.client.login(username='testteacher', password='password')
        self.course = Course.objects.create(
            name='Test Teacher Course', 
            description='Test Course Description', 
            created_by=self.user, 
            duration=100,
            category_id=self.category.id,
            places_count=10,
            created_at=datetime.strptime("10-08-2025", "%d-%m-%Y").date(),
            start_date=datetime.strptime("10-08-2025", "%d-%m-%Y").date(),
            end_date=datetime.strptime("20-09-2025", "%d-%m-%Y").date()   
        )

    def test_teacher_profile_page(self):
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)

class UserProfileViewStudentTestCase(TestCase):

    def setUp(self):
        self.user = Users.objects.create_user(username='teststudent', password='password')
        self.client.login(username='teststudent', password='password')
        self.category = Category.objects.create(name='A', title="adasd", description='sdfsdf')
        self.course = Course.objects.create(
            name='Test Teacher Course', 
            description='Test Course Description', 
            created_by=self.user, 
            duration=100,
            category_id=self.category.id,
            places_count=10,
            created_at=datetime.strptime("10-08-2025", "%d-%m-%Y").date(),
            start_date=datetime.strptime("10-08-2025", "%d-%m-%Y").date(),
            end_date=datetime.strptime("20-09-2025", "%d-%m-%Y").date()   
        )
        self.enrollment = Enrollment.objects.create(student=self.user, course=self.course)

    def test_student_profile_page(self):
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
