from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

tasks = []

def tasks_view(request):
    return render(request,"tasks.html",{"tasks" : tasks})

def add_task_view(request):
    tasks_value = request.GET.get("task")
    tasks.append(tasks_value)
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index):
    del tasks[index-1]
    return HttpResponseRedirect("/tasks")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/',tasks_view),
    path('tasks/add-task', add_task_view),
    path('tasks/delete-task/<int:index>', delete_task_view)
]
