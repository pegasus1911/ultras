from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('groups/', views.group_index, name='group-index'),
    path('groups/<int:group_id>/', views.group_detail, name='group-detail'),
]
