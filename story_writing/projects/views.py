from django.http import HttpResponse
from django.template import loader
from .models import Project, Chapter
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, get_object_or_404
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
        allchapters = project.chapter_set.all()
        template = loader.get_template('details.html')
        context = {
            'project': project,
            'allchapters': allchapters,
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
    if not request.user.is_authenticated:
        return redirect('login')

    allprojects = Project.objects.filter(user=request.user)

    chapters_by_project = {}
    for project in allprojects:
        project_chapters = project.chapter_set.all()
        if project_chapters:
            chapters_by_project[project] = project_chapters

    template = loader.get_template('chapters.html')
    context = {
        'chapters_by_project': chapters_by_project,
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


def create_project_api(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        name = request.POST.get('name', '').strip()
        if name and len(name) <= 255:
            Project.objects.create(
                name=name,
                user=request.user
            )
    return redirect('projects')


def delete_project_api(request):
    if request.method == 'POST' and request.user.is_authenticated:
        project_id = request.POST.get('project_id')
        try:
            project = Project.objects.get(id=project_id, user=request.user)
            project.delete()
        except (Project.DoesNotExist, ValueError):
            pass
    return redirect('projects')


def create_chapter_api(request, project_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        title = request.POST.get('title', '').strip()

        if title:
            try:
                project = Project.objects.get(id=project_id, user=request.user)

                last_chapter = Chapter.objects.filter(project=project).order_by('order').last()
                order = 0
                if last_chapter:
                    order = last_chapter.order + 1

                Chapter.objects.create(
                    title=title,
                    content='',
                    project=project,
                    order=order
                )

            except Project.DoesNotExist:
                pass

    return redirect('details', id=project_id)


def delete_chapter_api(request, project_id):
    if request.method == 'POST' and request.user.is_authenticated:
        project = get_object_or_404(Project, id=project_id, user=request.user)
        chapter_id = request.POST.get('chapter_id')

        if chapter_id:
            try:
                chapter = project.chapter_set.get(id=chapter_id)
                chapter.delete()
            except Chapter.DoesNotExist:
                pass

    return redirect('details', id=project_id)
