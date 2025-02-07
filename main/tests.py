from datetime import datetime
from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth.models import User

from users.models import Users
from .models import Course, Category, Enrollment
from django.utils import timezone


class CourseViewsTest(TestCase):
    def setUp(self):
        
        self.category = Category.objects.create(name='A', title="adasd", description='sdfsdf')
        self.create_user = Users.objects.create(username="Oleg", password="12345" )
        
        self.course = Course.objects.create(
            name='Test Teacher Course', 
            description='Test Course Description', 
            created_by=self.create_user, 
            duration=100,
            category_id=self.category.id,
            places_count=10,
            created_at=datetime.strptime("10-08-2025", "%d-%m-%Y").date(),
            start_date=datetime.strptime("10-08-2025", "%d-%m-%Y").date(),
            end_date=datetime.strptime("20-09-2025", "%d-%m-%Y").date()   
        )
        
        self.user = Users.objects.create(username="testuser", password="testpassword")
        
        self.enrollment = Enrollment.objects.create(course=self.course, student=self.user)

    def test_home_view(self):
        """Test if the home page loads correctly and displays the categories."""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main.html')
        self.assertContains(response, self.category.name)