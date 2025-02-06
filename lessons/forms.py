from django import forms
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
        self.user = kwargs.pop('user', Users)
        super(LessonEnrollmentForm, self).__init__(*args, **kwargs)

        if self.user and self.user.is_instructor():
            self.fields['instructor'].widget = forms.HiddenInput()
            self.fields['instructor'].initial = self.user.id
        elif self.user and self.user.is_admin():
            pass