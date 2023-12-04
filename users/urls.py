from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.perfil, name='user'),
    path('edit',views.UserEditView , name="edit"),
    path('delete',views.UserDeleteView , name="delete"),
    path('list',views.UserListView, name="list"),
    
]