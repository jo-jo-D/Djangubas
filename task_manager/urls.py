from django.urls import path
from .views import create_task, get_info, get_id_task, get_stats


urlpatterns = [
    path('tasks/create/', create_task, name='create a task'),
    path('tasks/info/', get_info, name='get task info'),
    path('task/<int:id>/', get_id_task, name='get task info'),
    path('tasks/stats/', get_stats, name='get stats of the all tasks'),
]