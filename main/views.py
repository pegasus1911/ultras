from django.shortcuts import render
from django.http import HttpResponse
from .models import Group

from django.shortcuts import render
from .models import Group

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def group_index(request):
    groups = Group.objects.all() 
    return render(request, 'groups/index.html', {'groups': groups})

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    return render(request, 'groups/detail.html', {'group': group})
