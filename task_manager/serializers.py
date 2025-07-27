from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import Task, SubTask, Category
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'status', 'deadline', 'description']
        model = Task

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['title', 'task', 'status', 'deadline', 'description', 'created_at']


class CategoryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=Category.objects.all())])

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise ValidationError('Category with such name already exists.')
        return super().create(validated_data)


    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if Category.objects.filter(name=name).exists():
            raise ValidationError('Category with such name already exists.')
        return super().update(instance, validated_data)

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        if value < timezone.now():
            raise ValidationError('Task deadline cannot be in the past.')
        return value