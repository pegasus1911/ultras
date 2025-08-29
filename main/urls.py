from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('groups/', views.group_index, name='group-index'),
    path('groups/<int:group_id>/', views.group_detail, name='group-detail'),
    path('groups/create/', views.GroupCreate.as_view(), name='group-create'),
    path('groups/<int:pk>/update/', views.GroupUpdate.as_view(), name='group-update'),
    path('groups/<int:pk>/delete/', views.GroupDelete.as_view(), name='group-delete'),
    path('groups/<int:group_id>/add-tifo/', views.add_tifo, name='add-tifo'),

]
