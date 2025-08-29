from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('groups/', views.group_index, name='group-index'),
    path('groups/create/', views.GroupCreate.as_view(), name='group-create'),
    path('groups/<int:pk>/update/', views.GroupUpdate.as_view(), name='group-update'),
    path('groups/<int:pk>/delete/', views.GroupDelete.as_view(), name='group-delete'),
    path('groups/<int:group_id>/', views.group_detail, name='group-detail'),
    path('groups/<int:group_id>/tifo/create/', views.tifo_create, name='tifo-create'),
    path('tifo/<int:tifo_id>/edit/', views.tifo_edit, name='tifo-edit'),
    path('tifo/<int:tifo_id>/delete/', views.tifo_delete, name='tifo-delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/',LoginView.as_view(template_name='registration/login.html', next_page='home'),name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('countries/', views.countries_list, name='countries-index'),
    path('countries/<int:country_id>/', views.country_detail, name='country-detail'),
]
