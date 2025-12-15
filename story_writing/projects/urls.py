from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name='main'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project_api, name='create_project_api'),
    path('projects/details/<int:id>', views.details, name='details'),
    path('projects/details/<int:id>/chapters', views.chapters, name='chapters'),
    path('projects/details/<int:id>/characters', views.characters, name='characters'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('delete_project_api/', views.delete_project_api, name='delete_project_api'),
    path('details/<int:project_id>/create_chapter/', views.create_chapter_api, name='create_chapter_api'),
    path('details/<int:project_id>/delete_chapter/', views.delete_chapter_api, name='delete_chapter_api'),
]
