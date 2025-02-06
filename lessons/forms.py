from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import LessonEnrollment
from users.models import Users

class LessonEnrollmentForm(forms.ModelForm):
    class Meta:
        model = LessonEnrollment
        fields = ['date', 'instructor', 'car_brand', 'car_number']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LessonEnrollmentForm, self).__init__(*args, **kwargs)

        self.fields['instructor'].queryset = Users.objects.filter(role='instructor')

        if self.user and self.user.is_instructor():
            self.fields['instructor'].widget = forms.HiddenInput()
            self.fields['instructor'].initial = self.user.id
        elif self.user and self.user.is_admin():
            pass

    def clean_date(self):
        """
        Валидация даты: дата не может быть раньше текущей.
        """
        selected_date = self.cleaned_data.get('date')
        if selected_date and selected_date < date.today():
            raise ValidationError("Дата не может быть раньше текущей.")
        return selected_date