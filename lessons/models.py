from django.db import models
from django.core.validators import RegexValidator
from users.models import Users

class LessonEnrollment(models.Model):
    date = models.DateField()
    instructor = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='instructor_lessons'
    )
    student = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_lessons'
    )
    is_booked = models.BooleanField(default=False)

    # Новые поля с значениями по умолчанию
    car_brand = models.CharField(max_length=50, verbose_name="Марка машины", default="Не указано")
    car_number = models.CharField(
        max_length=10,
        verbose_name="Гос номер машины",
        validators=[
            RegexValidator(
                regex=r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$',
                message="Гос номер должен быть в формате: А123БВ45 или А123БВ456"
            )
        ],
        default="А000АА00"  # Значение по умолчанию для гос номера
    )

    def __str__(self):
        if self.student:
            return f"Registration {self.id} - {self.student} on {self.date}"
        else:
            return f"Registration {self.id} - Available on {self.date}"