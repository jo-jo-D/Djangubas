from django.db.models.functions import ExtractWeekDay
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from task_manager.models import Task, SubTask, Category, Category
from task_manager.serializers import TaskSerializer, SubTaskCreateSerializer, CategoryCreateSerializer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, filters, serializers
from django.db.models import Q, Count
from django.utils import timezone

from .permissions import IsAdminOrReadOnly
from .serializers import SubTaskSerializer
from rest_framework.pagination import PageNumberPagination

class BaseListCreateView(ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at', ]

class TaskListCreateView(BaseListCreateView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Task.objects.all()
        day_to_filter_by = self.request.query_params.get('weekday')

        if day_to_filter_by:
            try:
                day_to_filter_by = int(day_to_filter_by)
                if not (1 <= day_to_filter_by <= 7):
                    raise ValueError("Weekday must be between 1 (Sunday) and 7 (Saturday)")
                queryset  = queryset.annotate(weekday=ExtractWeekDay('created_at')).filter(weekday=day_to_filter_by)
            except ValueError:
                raise serializers.ValidationError({"weekday": "Must be an integer between 1 and 7"})

        return queryset


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def get_stats(request):
    permission_classes = [IsAdminUser]

    amnt_info = Task.objects.count()

    task_status_dict = Task.objects.values('status').annotate(count=Count('id'))
    task_statuses = {i['status']: i['count'] for i in task_status_dict}

    overdued = Task.objects.filter(
        Q(deadline__lte=timezone.now()) & ~Q(status='Done')
    )
    overdued_serializer = TaskSerializer(overdued, many=True)

    stats = {
        'total_tasks': amnt_info,
        'overdue_tasks': overdued_serializer.data,
        'tasks_by_status': task_statuses,
    }

    return Response(data=stats, status=status.HTTP_200_OK)


class SubTaskListCreateView(BaseListCreateView):
    serializer_class = SubTaskCreateSerializer  #post уже реализован из коробки
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = SubTask.objects.all()
        task_title = self.request.query_params.get('task')
        status_param = self.request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title=task_title)
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated]

# class SubTaskDetailUpdateDeleteView(APIView):
#
#     def get_object(self, pk: int):
#         return get_object_or_404(SubTask, pk=pk)
#
#
#     def get(self, request, pk: int):
#         obj = self.get_object(pk)
#         serializer = SubTaskSerializer(obj, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
#     def put(self, request, pk: int):
#         obj = self.get_object(pk)
#         serializer = SubTaskCreateSerializer(obj, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     def patch(self, request, pk: int):
#         obj = self.get_object(pk)
#         serializer = SubTaskCreateSerializer(obj, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     def delete(self, request, pk: int):
#         obj = self.get_object(pk)
#         obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class TaskFilteredListView(APIView):
#     def get(self, request):
#         day_to_filter_by = request.query_params.get('weekday')
#
#         tasks = Task.objects.all()  #переопределяется если есть параметры, нет - сериализ. старую версию и выдает список
#
#         if day_to_filter_by:
#             try:
#                 day_to_filter_by = int(day_to_filter_by)
#                 if not (1 <= day_to_filter_by <= 7):
#                     return Response(
#                         {"error": "day_to_filter_by must be between 1 (sunday) and 7 (monday)"},
#                         status=status.HTTP_400_BAD_REQUEST)
#                 tasks = tasks.annotate(weekday=ExtractWeekDay('created_at')).filter(weekday=day_to_filter_by)
#
#             except ValueError:
#                 return Response({"error":"day_to_filter_by must be represented as an integer"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = TaskSerializer(tasks, many=True)
#         return  Response(serializer.data, status=status.HTTP_200_OK)
#

# class SubTaskListCreateView(APIView):       #SRP
#     def get(self, request):
#
#         def paginate_and_respond(queryset):
#             paginator = PageNumberPagination()
#             paginator.page_size = 5
#             page = paginator.paginate_queryset(queryset, request)
#             serializer = SubTaskSerializer(page, many=True)
#             return paginator.get_paginated_response(serializer.data)
#
#         params = {}
#         main_task_title = request.query_params.get('task', None)
#         subtask_status = request.query_params.get('status', None)
#         if main_task_title:
#             params['task__title'] = main_task_title
#         if subtask_status:
#             params['status'] = subtask_status
#
#         queryset = SubTask.objects.filter(**params) if params else SubTask.objects.all()
#
#         if not queryset.exists():
#             return Response(data=[], status=status.HTTP_204_NO_CONTENT)
#
#         return paginate_and_respond(queryset)
#
#
#     def post(self, request):
#             serializer = SubTaskSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        category_with_counted_tasks = Category.objects.annotate(task_count=Count('tasks'))

        data = [
            {
                "id":category.id,
                "category": category.name,
                "task_count":category.task_count,
            } for category in category_with_counted_tasks
        ]
        return Response(data=data, status=status.HTTP_200_OK)
