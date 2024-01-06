from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tasks.models import Task
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

class AuthorisedTaskManager(LoginRequiredMixin):
     def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class UserLoginView(LoginView):
    template_name = "user_login.html"
 
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = "/user/login"

def session_storage_view(request):
    total_views = request.session.get("total_views", 0)
    request.session["total_views"] = total_views + 1
    return HttpResponse("Total views: {} The user is {}".format(total_views, request.user.is_authenticated))

class GenericTaskDetailView(AuthorisedTaskManager, DetailView):
    model = Task
    template_name = "task_detail.html"

class TaskCreateForm(ModelForm):

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 4:
            raise ValidationError("Title must be at least 5 characters long")
        return title
    class Meta:
        model = Task
        fields = ("title", "description", "completed")

class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_update.html"
    success_url = "/tasks"

class TaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "delete_task.html"
    success_url = "/tasks"            

class GenericTaskCreateView(CreateView):
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = "/tasks"
    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class GenericTaskView(LoginRequiredMixin,ListView):
    queryset = Task.objects.filter(completed=False).filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(completed=False).filter(deleted=False).filter(user=self.request.user)
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks

class CreateTaskView(View):
    def get(self, request):
        return render(request, "task_create.html")
    
    def post(self,request):
        Task(title = request.POST.get("task")).save()
        return HttpResponseRedirect("/tasks")
       
class TaskCompleteView(AuthorisedTaskManager, UpdateView):
    model = Task
    template_name = "complete_task.html"
    fields = ['completed']  
    
    def get_success_url(self):
        return "/tasks"  

    def form_valid(self, form):
        task = form.save(commit=False)
        task.completed = True
        task.save()
        return HttpResponseRedirect(self.get_success_url())

class CompletedTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "completed_tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        print(Task.objects.filter(deleted=False, user = self.request.user))
        return Task.objects.filter(completed=True, deleted=False, user = self.request.user)
