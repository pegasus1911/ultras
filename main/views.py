from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from .models import Group, Tifo, Country
from .forms import TifoForm
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('group-index')
        else:
            error_message = 'wrongg sign up pleaase try again'
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})
@login_required
def group_index(request):
    groups = Group.objects.all()
    return render(request, 'groups/groups.html', {'groups': groups})
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    tifos = group.tifo_set.all()
    tifo_form = TifoForm()
    return render(request, 'groups/detail.html', {
        'group': group,
        'tifos': tifos,
        'tifo_form': tifo_form
    })
class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'founding_year', 'description', 'logo', 'country']
    template_name = 'groups/group_form.html'
class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    fields = ['name', 'founding_year', 'description', 'logo', 'country']
    template_name = 'groups/group_form.html'
class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = '/groups/'
    template_name = 'groups/group_confirm_delete.html'
@login_required
def tifo_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = TifoForm(request.POST, request.FILES)
        if form.is_valid():
            tifo = form.save(commit=False)
            tifo.group = group
            tifo.user = request.user
            tifo.save()
            return redirect('group-detail', group_id=group.id)
    else:
        form = TifoForm()
    return render(request, 'tifos/tifo_form.html', {'form': form, 'group': group})
@login_required
def tifo_edit(request, tifo_id):
    tifo = get_object_or_404(Tifo, id=tifo_id)
    if tifo.user != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = TifoForm(request.POST, request.FILES, instance=tifo)
        if form.is_valid():
            form.save()
            return redirect('group-detail', group_id=tifo.group.id)
    else:
        form = TifoForm(instance=tifo)
    return render(request, 'tifos/tifo_form.html', {'form': form, 'group': tifo.group, 'edit': True})
@login_required
def tifo_delete(request, tifo_id):
    tifo = get_object_or_404(Tifo, id=tifo_id)
    if tifo.user != request.user:
        raise PermissionDenied
    tifo.delete()
    return redirect('group-detail', group_id=tifo.group.id)
@login_required
def tifo_detail(request, tifo_id):
    tifo = get_object_or_404(Tifo, id=tifo_id)
    return render(request, 'tifos/detail.html', {'tifo': tifo})
@login_required
def countries_list(request):
    query = request.GET.get('q', '')
    countries = Country.objects.filter(name__icontains=query) if query else Country.objects.all()
    return render(request, 'main/countries.html', {'countries': countries, 'query': query})
@login_required
def country_detail(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    groups = country.groups.all()
    return render(request, 'main/country_detail.html', {'country': country, 'groups': groups})
