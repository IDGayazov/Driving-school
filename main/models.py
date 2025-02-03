from django.db import models

from users.models import Users

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    duration = models.IntegerField()
    places_count = models.IntegerField()
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    
    
class Enrollment(models.Model):
    student = models.ForeignKey(Users, on_delete=models.CASCADE) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"
