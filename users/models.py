from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('teacher', 'Teacher'),
    ]

    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def has_role(self, role):
        return self.role == role


    def is_admin(self):
        return self.has_role('admin')


    def is_student(self):
        return self.has_role('student')


    def is_instructor(self):
        return self.has_role('instructor')


    def is_teacher(self):
        return self.has_role('teacher')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    