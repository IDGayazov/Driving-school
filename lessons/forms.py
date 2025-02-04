from django import forms
from .models import LessonEnrollment

class LessonEnrollmentForm(forms.ModelForm):
    class Meta:
        model = LessonEnrollment
        fields = ['date', 'instructor']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
