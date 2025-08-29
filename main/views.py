from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Group, Tifo
from .forms import TifoForm


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
    tifo_form = TifoForm()
    return render(request, 'groups/detail.html', {
        'group': group,
        'tifo_form': tifo_form
    })
def add_tifo(request, group_id):
    form = TifoForm(request.POST)
    if form.is_valid():
        new_tifo = form.save(commit=False)
        new_tifo.group_id = group_id
        new_tifo.save()
    return redirect('group-detail', group_id=group_id)

class GroupCreate(CreateView):
    model = Group
    fields = '__all__'

class GroupUpdate(UpdateView):
    model = Group
    fields = ['country', 'founding_year', 'description']  # name stays locked

class GroupDelete(DeleteView):
    model = Group
    success_url = '/groups/'
