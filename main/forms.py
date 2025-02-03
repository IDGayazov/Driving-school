from django import forms
from .models import Enrollment, Course

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # if user:
        #     self.fields['course'].queryset = Course.objects.filter(
        #         places_count__gt=Enrollment.objects.filter(course__student=user).count()
        #     )