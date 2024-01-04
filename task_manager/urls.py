from django.contrib import admin
from django.urls import path

from tasks.views import (add_task_view, all_tasks_view, complete_task_view, completed_tasks_view, delete_task_view, 
                         GenericTaskView, GenericTaskCreateView, GenericTaskUpdateView, session_storage_view, UserCreateView,
                         UserLoginView)

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', GenericTaskView.as_view()),
    path('add-task/', add_task_view),
    path('create-task/', GenericTaskCreateView.as_view()),
    path('update-task/<int:pk>/', GenericTaskUpdateView.as_view()),
    path('delete-task/<int:index>/', delete_task_view),
    path('complete_task/<int:index>/', complete_task_view),
    path('completed_tasks/', completed_tasks_view),
    path('all_tasks/', all_tasks_view),
    path('sessiontest',session_storage_view),
    path('user/signup', UserCreateView.as_view()),
    path('user/login', UserLoginView.as_view()),
    path('user/logout', LogoutView.as_view()), 
]