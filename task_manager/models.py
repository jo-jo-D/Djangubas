from django.utils import timezone
from datetime import timedelta
from django.db import models
from .managers import SoftDeleteManager
from django.contrib.auth.models import User


STATUS_CHOICES = {
    'new': 'New',
    'in_progress': 'In Progress',
    'completed': 'Done',
    'blocked': 'Blocked',
    'failed': 'Failed',
    'pending': 'Pending',
}

def default_deadline():
    return timezone.now() + timedelta(weeks=1)

class Task(models.Model):
    title = models.CharField(max_length=100, unique_for_date="deadline")
    # subtasks = models.ManyToManyField("SubTask", related_name="tasks")
    description = models.TextField()
    categories = models.ManyToManyField('Category', related_name='tasks', verbose_name="Category of the task")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status of the task")
    deadline = models.DateTimeField(default=default_deadline, verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    owner = models.ForeignKey(User, verbose_name='owner', related_name='tasks',  on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title}, till {self.deadline.date()}"

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        unique_together = ('title',)


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(choices=STATUS_CHOICES, default='new', verbose_name="Status of the subtask")
    deadline = models.DateTimeField(default=default_deadline, verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    owner = models.ForeignKey(User, verbose_name='owner', related_name='subtasks', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title}(regarding: '{self.task.title}', till {self.task.deadline.date()})"

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Subtask'
        unique_together = ('title',)

TASK_CATEGORIES = [
    ('work', 'Work'),
    ('personal', 'Personal'),
    ('home', 'Home'),
    ('health', 'Health'),
    ('finance', 'Finance'),
    ('study', 'Study / Education'),
    ('meetings', 'Meetings'),
    ('shopping', 'Shopping'),
    ('travel', 'Travel'),
    ('other', 'others'),
]

class Category(models.Model):
    name = models.CharField(max_length=50, choices=TASK_CATEGORIES, verbose_name="category of the task")
    is_deleted = models.BooleanField(default=False, verbose_name="is deleted")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="deleted at")
    restored_at = models.DateTimeField(null=True, blank=True, verbose_name="restored at")

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.restored_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.name}"


    class Meta:
        db_table = 'task_manager_category'
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        unique_together = ('name',)