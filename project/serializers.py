from rest_framework import serializers

from project.models import Project, Task


class ProjectListSerializer(serializers.ModelSerializer):
    """ Для сериализации нескольких объектов Project """

    class Meta:
        model = Project
        fields = ['id', 'name', 'description']


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [ 'id', 'name', 'description']