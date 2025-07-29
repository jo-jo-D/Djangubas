from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (get_stats, TaskDetailUpdateDeleteView, CategoryViewSet,
                    SubTaskListCreateView, SubTaskDetailUpdateDeleteView, TaskListCreateView)

router = DefaultRouter()
router.register('category/', CategoryViewSet, basename='category')

urlpatterns = [
    path('tasks/stats/', get_stats, name='get stats of the all tasks'),
    # path('tasks/weekday/<int:day_to_filter_by>', TaskFilteredListView.as_view(), name='Tasks filtered by weekday'),
    path('tasks/', TaskListCreateView.as_view(), name='List of all the tasks, creation or add /?weekday=2 to filter'),
    path('task/<int:pk>/', TaskDetailUpdateDeleteView.as_view(), name='Task Detail Update Delete'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='SubTasks list and creation'),
    path('subtask/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='Get details, modify or delete concrete subtask.'),
    path('', include(router.urls))
]

