from django.db import models

LANG_CHOICES = {
    'py': 'Python',
    'js': 'JavaScript',
    'c#': 'C#',
    'c++': 'C++',
    'java': 'Java',
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
class Tag(models.Model):

    name = models.CharField(max_length=100, choices=TAG_CHOICES)        #по дефолту без вербоза будет имя колонки как имя переменной
    projects = models.ManyToManyField('Project', related_name='tags')

class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    lang = models.CharField(choices=LANG_CHOICES.items())

class Dev(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(choices= RANK_CHOICES)
    projects = models.ManyToManyField('Project', related_name='devs')