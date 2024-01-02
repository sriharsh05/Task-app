from django.contrib import admin
from django.urls import path

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

tasks = []
completed_tasks = []

def tasks_view(request):
    return render(request,"tasks.html",{"tasks" : tasks})

def add_task_view(request):
    tasks_value = request.GET.get("task")
    tasks.append(tasks_value)
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index):
    del tasks[index-1]
    return HttpResponseRedirect("/tasks")

def completed_tasks_view(request):
    return render(request, "completed_tasks.html", {"completed_tasks" : completed_tasks})

def all_tasks_view(request):
    return render(request, "all_tasks.html", {"completed_tasks" : completed_tasks, "tasks" : tasks})

def complete_task_view(request, index):
    completed_tasks.append(tasks.pop(index-1))
    return HttpResponseRedirect("/tasks")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', tasks_view),
    path('add-task/', add_task_view),
    path('delete-task/<int:index>/', delete_task_view),
    path('complete_task/<int:index>/', complete_task_view),
    path('completed_tasks/', completed_tasks_view),
    path('all_tasks/', all_tasks_view),
]