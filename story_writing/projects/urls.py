from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name='main'),
    path('projects/', views.projects, name='projects'),
    path('projects/details/<int:id>', views.details, name='details'),
    path('projects/details/<int:id>/chapters', views.chapters, name='chapters'),
    path('projects/details/<int:id>/characters', views.characters, name='characters'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]
