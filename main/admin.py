from django.contrib import admin

from main.models import Course, Category, Enrollment

# Register your models here.
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Enrollment)