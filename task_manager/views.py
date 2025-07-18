from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from task_manager.models import Task, SubTask
from task_manager.serializers import TaskSerializer, SubTaskCreateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count
from django.utils import timezone
from .serializers import SubTaskSerializer


@api_view(['GET', 'POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_info(request):
    info = Task.objects.all()
    if info.exists():
        serializer = TaskSerializer(info, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data={'details': 'No data found'}, status=status.HTTP_200_OK)   # потому что отсутствие данных в бд не ошибка

@api_view(['GET'])
def get_id_task(request, id):
    try:
        id_task = Task.objects.get(id=id)
        serializer = TaskSerializer(id_task, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response(data={'details': 'No data found' }, status=status.HTTP_404_NOT_FOUND)
'''          Если поиск не по полю с первичным ключем добавить это          '''
    # except Task.MultipleObjectsReturned:
    #     return Response(data={'details':'Multiple objects found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_stats(request):
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


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()

        if not subtasks.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)

        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):

    def get_object(self, pk: int):
        return get_object_or_404(SubTask, pk=pk)


    def get(self, request, pk: int):
        obj = self.get_object(pk)
        serializer = SubTaskSerializer(obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk: int):
        obj = self.get_object(pk)
        serializer = SubTaskCreateSerializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk: int):
        obj = self.get_object(pk)
        serializer = SubTaskCreateSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk: int):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
