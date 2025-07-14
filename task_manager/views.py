from task_manager.models import Task
from task_manager.serializers import TaskSerializer
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count
from django.utils import timezone


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
