from django.http import HttpResponse
from django.template import loader
from .models import Project
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm


def projects(request):
    if request.user.is_authenticated:
        allprojects = Project.objects.filter(user=request.user)
    else:
        allprojects = Project.objects.none()

    template = loader.get_template('all_projects.html')
    context = {
        'allprojects': allprojects,
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    project = Project.objects.get(id=id)
    if request.user.is_authenticated and project.user == request.user:
        template = loader.get_template('details.html')
        context = {
            'project': project,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('main')


def main(request):
    template = loader.get_template('main.html')
    context = {
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))


def chapters(request):
    template = loader.get_template('chapters.html')
    context = {
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))


def characters(request):
    template = loader.get_template('characters.html')
    context = {
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()

    template = loader.get_template('register.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def logout(request):
    auth_logout(request)
    return redirect('main')
