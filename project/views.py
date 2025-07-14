#from django.shortcuts import render
#from django.core.paginator import Paginator
# Create your views here.
#from django.utils import timezone

from rest_framework.decorators import api_view
from project.models import Project, Task
from project.serializers import ProjectListSerializer, TaskListSerializer
from rest_framework.response import Response
from rest_framework import status


def test(req):
    pass

@api_view(['GET'])
def list_project(request):
    projects = Project.objects.all()
    if projects.exists():
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message':'Project NOT found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_task(request):
    tasks = Task.objects.all()
    if tasks.exists():
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
