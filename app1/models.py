import uuid

from django.db import models


class User(models.Model):

    countries = {
        'US': 'United States',
        'FR': 'France',
        'DE': 'Germany',
    }

    name = models.CharField(max_length=70, null=False, blank=False)
    last_name = models.CharField(max_length=70)
    age = models.IntegerField()
    rating = models.FloatField(default=0)
    country = models.CharField(choices=countries, default='FR', help_text='Where are you from?')
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    married = models.BooleanField(default=False)

class Actor(models.Model):
    name = models.CharField(max_length=70, null=False, blank=False)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)
    experience = models.IntegerField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=70, null=False, blank=False)
    actors = models.ManyToManyField(Actor, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name='movies')

    def __str__(self):
        if self.Director:
            return f"'{self.title}'. {self.director.name}"
        else:
            return self.title


