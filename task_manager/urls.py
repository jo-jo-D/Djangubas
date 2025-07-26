from django.urls import path
from .views import (create_task, get_info, get_id_task, get_stats, TaskFilteredListView,
                    SubTaskListCreateView, SubTaskDetailUpdateDeleteView)


urlpatterns = [
    path('tasks/create/', create_task, name='create a task'),
    path('tasks/info/', get_info, name='get task info'),
    path('task/<int:id>/', get_id_task, name='get task info'),
    path('tasks/stats/', get_stats, name='get stats of the all tasks'),
    # path('tasks/weekday/<int:day_to_filter_by>', TaskFilteredListView.as_view(), name='Tasks filtered by weekday'),
    path('tasks/', TaskFilteredListView.as_view(), name='List of all the tasks or add /?weekday=2 to filter'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='Sub tasks list'),
    path('subtask/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='Get details, modify or delete concrete subtask.'),
]