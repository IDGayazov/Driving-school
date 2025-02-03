from django.db import models
from users.models import Users

class LessonEnrollment(models.Model):
    date = models.DateField()
    instructor = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='instructor_lessons'  # Уникальное имя для обратной связи
    )
    student = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_lessons'  # Уникальное имя для обратной связи
    )
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        if self.student:
            return f"Registration {self.id} - {self.student} on {self.date}"
        else:
            return f"Registration {self.id} - Available on {self.date}"