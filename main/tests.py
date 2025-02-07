from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth.models import User

from users.models import Users
from .models import Course, Category, Enrollment
from django.utils import timezone


class CourseViewsTest(TestCase):
    def setUp(self):
        # Create categories
        self.category = Category.objects.create(name="Python")
        self.create_user = Users.objects.create(username="Oleg", password="12345" )
        
        # Create courses
        self.course = Course.objects.create(
            name="Intro to Python",
            description="Learn Python from scratch",
            duration=30,
            price=20000,
            created_at=timezone.now(),
            created_by=self.create_user,
            category=self.category,
            places_count=10
        )
        
        # Create a user for login
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Create an enrollment for testing
        self.enrollment = Enrollment.objects.create(course=self.course, student=self.user)

    def test_home_view(self):
        """Test if the home page loads correctly and displays the categories."""
        response = self.client.get(reverse('main:home'))  # Assuming the URL name is 'main:home'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main.html')
        self.assertContains(response, self.category.name)

    def test_enroll_in_course_view(self):
        """Test if a user can enroll in a course."""
        self.client.login(username="testuser", password="testpassword")
        
        # Check if course enrollment is successful
        response = self.client.post(reverse('main:enroll_in_course', args=[self.course.id]))
        
        self.assertEqual(response.status_code, 302)  # Should redirect to the home page
        self.assertRedirects(response, reverse('main:home'))
        
        # Verify the number of places decreases after enrollment
        self.course.refresh_from_db()
        self.assertEqual(self.course.places_count, 9)
        
        # Verify that the user is enrolled
        self.assertTrue(Enrollment.objects.filter(course=self.course, student=self.user).exists())

    def test_category_detail_view(self):
        """Test if the category detail page loads correctly."""
        self.client.login(username="testuser", password="testpassword")
        
        # Go to category detail page
        response = self.client.get(reverse('main:category_detail', args=[self.category.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/category_detail.html')
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.course.title)
        
        # Check if the user is enrolled in the course
        self.assertIn(self.course.id, response.context['enrolled'])

    def test_category_detail_view_not_enrolled(self):
        """Test if the category detail page correctly reflects a user not enrolled in a course."""
        # Create a new user who is not enrolled in the course
        other_user = User.objects.create_user(username="otheruser", password="otherpassword")
        self.client.login(username="otheruser", password="otherpassword")
        
        # Go to category detail page
        response = self.client.get(reverse('main:category_detail', args=[self.category.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/category_detail.html')
        self.assertNotIn(self.course.id, response.context['enrolled'])

    def test_enroll_in_course_without_login(self):
        """Test if the user is redirected to login when not logged in."""
        response = self.client.post(reverse('main:enroll_in_course', args=[self.course.id]))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:enroll_in_course", args=[self.course.id])}')

