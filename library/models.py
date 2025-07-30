from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

from django.db.models import ForeignKey
from django.utils import timezone
from library.managers import SoftDeleteManager

class Author(models.Model):

    name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    date_of_birth = models.DateField(null=True, blank=True)
    profile = models.URLField(null=True, blank=True, verbose_name="Profile URL")
    deleted = models.BooleanField(default=False, help_text='If the author has been deleted from DB')
    rating = models.IntegerField(default=1, null=True, blank=True, verbose_name="Rating of the author",
                                 validators=[MinValueValidator(1), MaxValueValidator(10)]
                                 )

    def __str__(self):
        return f'{self.name} {self.last_name}'


GENRE_CHOICES ={'Fiction': 'Fiction',
                 'Non-Fiction': 'Non-Fiction',
                 'Science Fiction': 'Science Fiction',
                 'Fantasy': 'Fantasy',
                 'Mystery': 'Mystery',
                 'Biography': 'Biography',
                 'not set': 'not set',
                 }


# CATEGORY_CHOICES = [
#     ('education', 'Educational Literature'),
#     ('science', 'Popular Science'),
#     ('religion', 'Religious Literature'),
#     ('reference', 'Encyclopedias and Reference Books'),
#     ('children', 'Children’s Literature'),
#     ('professional', 'Professional Literature'),
#     ('self_help', 'Self-Help Books'),
#     ('travel', 'Travel Guides'),
#     ('art', 'Art and Design Books'),
#     ('biography', 'Biographies and Memoirs'),
# ]

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Book category", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True, default='publisher')
    established_date = models.DateField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, verbose_name="Genre", choices=GENRE_CHOICES)

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=70)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, default='Unknown', related_name='books')
    release_year = models.IntegerField('release date', default=datetime.date.today().year)
    summary = models.TextField(max_length=255, null=True, blank=True, verbose_name="Book summary")
    genres = models.ManyToManyField(Genre, related_name='books')
    pages = models.PositiveIntegerField(default=20, validators=[MaxValueValidator(10000)], verbose_name="Pages")
    categories = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    libraries = models.ManyToManyField('Library', related_name='books', verbose_name="Library")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Price")
    is_banned = models.BooleanField(default=False, verbose_name="Is Banned")
    is_deleted = models.BooleanField(default=False)  # Поле для мягкого удаления

    @property
    def rating(self):
        return self.reviews.all().aggregate(models.Avg('rating'))['rating__avg']

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """Переопределяем стандартный метод удаления."""
        self.is_deleted = True  # Устанавливаем флаг
        self.save()  # Сохраняем изменения

    def restore(self):
        """Метод для восстановления записи."""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{self.title} ({self.release_year})"


# class Publisher(models.Model):
#     name = models.CharField(max_length=70)
#     address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Address")
#     city = models.CharField(max_length=100, null=True, blank=True, verbose_name="City")
#     country = models.CharField(max_length=100, null=True, blank=True, verbose_name="Country")
#
#     def __str__(self):
#         return f"'{self.name}', {self.city}"


class Library(models.Model):
    title = models.CharField(max_length=70, blank=True, verbose_name="Library name")
    location = models.CharField(max_length=70, null=True, blank=True, verbose_name="Library location")
    website = models.URLField(null=True, blank=True, verbose_name="Library's website")


    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Libraries"

GENDER_CHOICES ={'M': 'Male',
                 'F': 'Female',
                 'Other': 'Other',
                 'ns': 'not set'}

ROLE_CHOICES={
    'admin':'Administrator',
    'editor':'Editor',
    'employee':'Employee',
    'staff':'Staff',
    'reader':'Reader',

}
class Member(models.Model):
    name = models.CharField(max_length=70, null=False, blank=False, verbose_name="Library member's name")
    last_name = models.CharField(max_length=70, null=False, blank=False, verbose_name="Library member's last name")
    email = models.EmailField(max_length=70, null=False, blank=False, verbose_name="Library member's email", unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, verbose_name="Gender", default='ns')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of birth")
    age = models.PositiveIntegerField(editable=False, verbose_name="Age")
    role = models.CharField(max_length=30, verbose_name='Role', choices=ROLE_CHOICES)
    active = models.BooleanField(default=True, verbose_name='Active')
    libraries = models.ManyToManyField('Library', related_name='members', verbose_name="Library")


    def save(self, *args, **kwargs):
        ages = timezone.now().year - self.date_of_birth.year
        if 6 <= ages <= 100:
            self.age = ages
            super().save(*args, **kwargs)

        else:
            raise ValidationError("Age must be between 6 and 100")


    def __str__(self):
        return f"{self.name} {self.last_name}"