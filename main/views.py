from django.shortcuts import render

from main.models import Category

def home(request):
    context = {
        "categories_list": Category.objects.get_queryset()
    }
    return render(request, 'main/main.html', context)