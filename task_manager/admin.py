from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from task_manager.models import Task, SubTask, Category

class SubTaskInline(admin.StackedInline):   # Inline for SubTask inside Task admin form
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "status", "deadline")
    list_filter = ("status",)
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return (obj.title[:10] +'...') if len(obj.title) > 10 else obj.title

    short_title.short_description = "Task title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "description")
    list_filter = ("status",)

    def completed(self, request, queryset):
        queryset.update(status='Done')

    completed.short_description = "Set as completed (Done)"

    def extend_the_deadline(self, request, queryset):
        queryset.update(deadline=timezone.now()+timedelta(days=2))

    extend_the_deadline.short_description = "Extend deadline for 2 days"

    actions = [completed, extend_the_deadline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
