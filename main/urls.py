from django.urls import path
from django.contrib.auth.decorators import login_required

from main.views import home, enroll_in_course, category_detail

app_name = 'main'

urlpatterns = [

    path('', home, name='home'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('enroll/<int:course_id>/', enroll_in_course, name='enroll_in_course'),
]