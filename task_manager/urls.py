from django.contrib import admin
from django.urls import path

from tasks.views import ( CompletedTaskListView, 
                         GenericTaskView, GenericTaskCreateView, GenericTaskUpdateView, session_storage_view, UserCreateView,
                         UserLoginView,TaskDeleteView, TaskCompleteView)

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', GenericTaskView.as_view()),
    path('create-task/', GenericTaskCreateView.as_view()),
    path('update-task/<int:pk>/', GenericTaskUpdateView.as_view()),
    path('delete-task/<pk>/', TaskDeleteView.as_view()),
    path('complete_task/<pk>/', TaskCompleteView.as_view()),
    path('completed_tasks/', CompletedTaskListView.as_view()),
    path('sessiontest',session_storage_view),
    path('user/signup', UserCreateView.as_view()),
    path('user/login', UserLoginView.as_view()),
    path('user/logout', LogoutView.as_view()), 
]