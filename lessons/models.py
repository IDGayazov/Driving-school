from django.db import models

from users.models import Users


class LessonEnrollment(models.Model):
    date = models.DateField()
    instructor = models.ForeignKey(Users, on_delete=models.CASCADE)
    student = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        if self.student:
            return f"Registration {self.unique_id} - {self.student} on {self.date}"
        else:
            return f"Registration {self.unique_id} - Available on {self.date}"