from django.utils import timezone
from datetime import timedelta

from django.db import models

# Модель Task:
# Описание: Задача для выполнения.
# Поля:
# title: Название задачи. Уникально для даты.
# description: Описание задачи.
# categories: Категории задачи. Многие ко многим.
# status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
# deadline: Дата и время дедлайн.
# created_at: Дата и время создания. Автоматическое заполнение.
STATUS_CHOICES = {
    'new': 'New',
    'in_progress': 'In Progress',
    'completed': 'Done',
    'blocked': 'Blocked',
    'failed': 'Failed',
    'pending': 'Pending',
}
class Task(models.Model):
    title = models.CharField(max_length=100, unique_for_date="deadline")
    # subtasks = models.ManyToManyField("SubTask", related_name="tasks")
    description = models.TextField()
    categories = models.ManyToManyField('Category', related_name='tasks', verbose_name="Category of the task")
    status = models.CharField(choices=STATUS_CHOICES, default='new', verbose_name="Status of the task")
    deadline = models.DateTimeField(default=timezone.now() + timedelta(weeks=1), verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return f"{self.title}, till {self.deadline.date()})"



# Модель SubTask:
# Описание: Отдельная часть основной задачи (Task).
# Поля:
# title: Название подзадачи.
# description: Описание подзадачи.
# task: Основная задача. Один ко многим.
# status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
# deadline: Дата и время дедлайн.
# created_at: Дата и время создания. Автоматическое заполнение.

class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='subtask')
    status = models.CharField(choices=STATUS_CHOICES, default='new', verbose_name="Status of the subtask")
    deadline = models.DateTimeField(default=timezone.now() + timedelta(weeks=1), verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return f"{self.title}(regarding: '{self.task.title}', till {self.task.deadline.date()})"

# Модель Category:
# Описание: Категория выполнения.
# Поля:
# name: Название категории.
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
    name = models.CharField(choices=TASK_CATEGORIES, verbose_name="Category of the task")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-name']
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'