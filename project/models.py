from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

LANG_CHOICES = {
    'py': '🐍Python',
    'js': 'JavaScript',
    'c#': 'C#',
    'c++': '➕C++',
    'java': '☕️Java',
}

TAG_CHOICES = {
    'frontend': 'FrontEnd',
    'backend': 'BackEnd',
    'Q&A': 'Q&A',
    'design': 'Design',
    'devops': 'DevOPS',
    'test': 'Test',
}

RANK_CHOICES = {
    'jun': 'Junior',
    'mid': 'Middle',
    'sen': 'Senior',
    'tl': 'Team-Lead',
}

STATUS_CHOICES = {
    'new': 'New',
    'in_progress': 'In Progress',
    'completed': 'Done',
    'blocked': 'Blocked',
    'failed': 'Failed',
    'pending': 'Pending',
}

PRIORITY_CHOICES = {
    'low': 'Low',
    'medium': 'Medium',
    'high': 'High',
    'critical': 'Critical',
}

class Tag(models.Model):

    name = models.CharField(max_length=100, choices=TAG_CHOICES, unique=True)        #по дефолту без вербоза будет имя колонки как имя переменной
    projects = models.ManyToManyField('Project', related_name='tags', blank=True)

    def __str__(self):
        return self.name


class Dev(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10, choices=RANK_CHOICES)
    projects = models.ManyToManyField('Project', related_name='devs', blank=True)

    def __str__(self):
        return f'🍒{self.name}🍒 ({self.grade} 👩🏽‍💻)'

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    lang = models.CharField(max_length=10, choices=LANG_CHOICES)
    dev = models.ForeignKey('Dev', on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(default=timezone.now)
    # tags = models.ManyToManyField(Tag, related_name='tasks',  blank=True, default=None)

    class Meta:
        ordering = ['-name']
        verbose_name_plural = 'Projects'
        verbose_name = 'Project'
        unique_together = (('name', 'description'),)


        # constraints = [
        #     models.CheckConstraint(condition=models.Q(name__icontains='project'), name='project_name__icontains')
        # ]
        #           icontains (и любые другие __lookup) нельзя использовать в CheckConstraint,
        #           потому что это работает только на уровне Django ORM, а CheckConstraint транслируется в SQL,
        #           где такие конструкции не работают.

    def __str__(self):
        return f'💻{self.name} 👩🏽‍💻({self.dev.name})'

class Task(models.Model):
    name = models.CharField(unique=True, validators=[MinLengthValidator(10)])
    description = models.CharField(null=True, blank=True, max_length=500)
    status = models.CharField(choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='low')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tasks',  blank=True)

    # relation to User model from django-models:
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)




