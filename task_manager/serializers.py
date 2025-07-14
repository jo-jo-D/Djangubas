from rest_framework import serializers
from .models import Task, SubTask

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'status', 'deadline', 'description']
        model = Task
