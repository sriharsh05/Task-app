from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task

def tasks_view(request):
    search_term = request.GET.get("search")
    tasks = Task.objects.filter(completed=False).filter(deleted=False)
    if search_term:
        tasks = tasks.filter(title__icontains=search_term)
    return render(request,"tasks.html",{"tasks" : tasks})

def add_task_view(request):
    Task(title = request.GET.get("task")).save()
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks")

def completed_tasks_view(request):
    completed_tasks = Task.objects.filter(completed=True).filter(deleted=False)
    return render(request, "completed_tasks.html", {"completed_tasks" : completed_tasks})

def all_tasks_view(request):
    tasks = Task.objects.filter(completed=False).filter(deleted=False)
    completed_tasks = Task.objects.filter(completed=True).filter(deleted=False)
    return render(request, "all_tasks.html", {"completed_tasks" : completed_tasks, "tasks" : tasks})

def complete_task_view(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/tasks")