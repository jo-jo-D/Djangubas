from django.contrib import admin
from task_manager.models import Task, SubTask, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "status", 'deadline')
    list_filter = ("status",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", 'description')
    list_filter = ("status",)
    # list_editable = ( 'description', 'task')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")