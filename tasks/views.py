from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from tasks.models import Task
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class TaskCreateForm(ModelForm):

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 4:
            raise ValidationError("Title must be at least 5 characters long")
        return title
    class Meta:
        model = Task
        fields = ("title", "description", "completed")
        

class GenericTaskCreateView(CreateView):
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = "/tasks"

class GenericTaskView(ListView):
    queryset = Task.objects.filter(completed=False).filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(completed=False).filter(deleted=False)
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks

class CreateTaskView(View):
    def get(self, request):
        return render(request, "task_create.html")
    
    def post(self,request):
        Task(title = request.POST.get("task")).save()
        return HttpResponseRedirect("/tasks")

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