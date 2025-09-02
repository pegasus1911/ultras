from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Country, Group, Tifo
from .forms import TifoForm
import uuid
import boto3
from django.conf import settings


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("group-index")
        else:
            error_message = "Sign up failed, try again"
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form, "error_message": error_message})



# @login_required
def countries_list(request):
    query = request.GET.get("q")
    if query:
        countries = Country.objects.filter(name__icontains=query)
    else:
        countries = Country.objects.all()
    return render(request, "main/countries.html", {"countries": countries, "query": query})


@login_required
def country_detail(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    groups = country.groups.all()
    return render(request, "main/country_detail.html", {"country": country, "groups": groups})

class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    fields = ["name", "founding_year", "description", "logo"]
    template_name = "groups/group_form.html"

    def form_valid(self, form):
        country_id = self.kwargs.get("country_id")
        country = get_object_or_404(Country, id=country_id)
        form.instance.country = country

        group = form.save(commit=False)

        logo_file = self.request.FILES.get('logo')
        if logo_file:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            key = uuid.uuid4().hex[:6] + logo_file.name[logo_file.name.rfind('.'):]
            s3.upload_fileobj(logo_file, settings.AWS_STORAGE_BUCKET_NAME, key)
            group.logo = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}'

        group.save()
        return redirect(f"/countries/{country.id}/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country_id = self.kwargs.get("country_id")
        context['country'] = get_object_or_404(Country, id=country_id)
        context['group'] = None
        return context

class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    fields = ["name", "founding_year", "description", "logo"]
    template_name = "groups/group_form.html"

    def form_valid(self, form):
        group = form.save(commit=False)

        logo_file = self.request.FILES.get('logo')
        if logo_file:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            key = uuid.uuid4().hex[:6] + logo_file.name[logo_file.name.rfind('.'):]
            s3.upload_fileobj(logo_file, settings.AWS_STORAGE_BUCKET_NAME, key)
            group.logo = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}'

        group.save()
        return redirect(f"/countries/{group.country.id}/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        context['country'] = self.object.country
        return context

class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "groups/group_confirm_delete.html"

    def get_success_url(self):
        return f"/countries/{self.object.country.id}/"


# @login_required
def group_index(request):
    groups = Group.objects.all()
    return render(request, "groups/groups.html", {"groups": groups})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    tifos = group.tifo_set.all()
    form = TifoForm()
    return render(request, "groups/detail.html", {"group": group, "tifos": tifos, "tifo_form": form})



@login_required
def tifo_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST":
        form = TifoForm(request.POST, request.FILES)
        if form.is_valid():
            tifo = form.save(commit=False)
            tifo.group = group
            tifo.user = request.user
            
            picture_file = request.FILES.get('picture')
            if picture_file:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                key = uuid.uuid4().hex[:6] + picture_file.name[picture_file.name.rfind('.'):]
                s3.upload_fileobj(picture_file, settings.AWS_STORAGE_BUCKET_NAME, key)
                tifo.picture = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}'

            tifo.save()
            return redirect("group-detail", group_id=group.id)
    else:
        form = TifoForm()
    return render(request, "tifos/tifo_form.html", {"form": form, "group": group})


@login_required
def tifo_detail(request, tifo_id):
    tifo = get_object_or_404(Tifo, id=tifo_id)
    return render(request, 'tifos/detail.html', {'tifo': tifo})

@login_required
def tifo_edit(request, tifo_id):
    tifo = get_object_or_404(Tifo, id=tifo_id)
    if tifo.user != request.user:
        return redirect("group-detail", group_id=tifo.group.id)

    if request.method == "POST":
        form = TifoForm(request.POST, request.FILES, instance=tifo)
        if form.is_valid():
            edited_tifo = form.save(commit=False)
            picture_file = request.FILES.get('picture')
            if picture_file:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                key = uuid.uuid4().hex[:6] + picture_file.name[picture_file.name.rfind('.'):]
                s3.upload_fileobj(picture_file, settings.AWS_STORAGE_BUCKET_NAME, key)
                edited_tifo.picture = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}'
            edited_tifo.save()
            return redirect("group-detail", group_id=tifo.group.id)
    else:
        form = TifoForm(instance=tifo)

    return render(request, "tifos/tifo_form.html", {"form": form, "group": tifo.group, "edit": True})


@login_required
def tifo_delete(request, tifo_id):
    tifo = get_object_or_404(Tifo, id=tifo_id)
    if tifo.user != request.user:
        return redirect("group-detail", group_id=tifo.group.id)

    if request.method == "POST":
        group_id = tifo.group.id
        tifo.delete()
        return redirect("group-detail", group_id=group_id)

    return render(request, "tifos/tifo_confirm_delete.html", {"tifo": tifo})
