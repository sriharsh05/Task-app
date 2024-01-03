from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task

tasks = []
completed_tasks = []

def tasks_view(request):
    search_term = request.GET.get("search")
    tasks = Task.objects.filter(deleted=False)
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
    return render(request, "completed_tasks.html", {"completed_tasks" : completed_tasks})

def all_tasks_view(request):
    return render(request, "all_tasks.html", {"completed_tasks" : completed_tasks, "tasks" : tasks})

def complete_task_view(request, index):
    completed_tasks.append(tasks.pop(index-1))
    return HttpResponseRedirect("/tasks")