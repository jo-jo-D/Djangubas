from django.contrib.auth.models import User
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
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Owner", null=True, related_name='books')

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


class Post(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at')
    title = models.CharField(max_length=255, unique_for_date='created_at', verbose_name="Title")
    text = models.TextField(null=False, blank=False, verbose_name="Text")
    author = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Author")
    moderated = models.BooleanField(default=False, verbose_name="Moderated?")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, verbose_name="Library")
    updated_at = models.DateTimeField(auto_now=True)


class Borrow(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Member")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name="Book")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, verbose_name="Library")
    book_take_date = models.DateField(auto_now_add=True, verbose_name="Book Take Date")
    book_return_date = models.DateField(verbose_name="Book Return Date")
    is_returned = models.BooleanField(default=False, verbose_name="Is returned?")

    def __str__(self):
        return f'{self.member.first_name} {self.member.last_name} took "{self.book.title}" on {self.book_take_date}'

    def check_to_date(self):
        if timezone.now().date() > self.book_return_date and self.is_returned == False:
            return True
        else:
            return False
    # use python manage.py shell
    # from library.models import Borrow
    # a = Borrow.object.get(pk=<borrow id>)
    # a.check_to_date()
    # result: True or False

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name="Book", related_name='reviews')
    reviewer = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Reviewer")
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Rating")
    review = models.TextField(verbose_name="Review")


class AuthorDetail(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name="Author")
    biography = models.TextField(verbose_name="Biography")
    city = models.CharField(verbose_name="City", max_length=50, null=True, blank=True)
    gender = models.CharField(verbose_name="Gender", max_length=20, choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name} from {self.city} born on {self.author.date_of_birth}.'


class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name="Event name")
    description = models.TextField(verbose_name="Event description")
    timestamp = models.DateTimeField(verbose_name="Event date")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, verbose_name="Library")
    book = models.ManyToManyField('Book', verbose_name="Books", related_name='events')

    def __str__(self):
        return f'{self.name} on {self.timestamp}'

class EventParticipant(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name="Event name")
    member = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Member")
    register_date = models.DateField(auto_now_add=True, verbose_name="Register date")

    def __str__(self):
        return f'{self.event.name}. Member: {self.member.first_name} {self.member.last_name} registered on {self.register_date}'


# creating a list of countries
countries = [
    ('DE', 'Germany'),
    ('UK', 'United Kingdom'),
    ('US', 'United States'),
    ('PT', 'Portugal'),
    ('FR', 'France'),
    ('ES', 'Spain'),
    ('IT', 'Italy'),
]

# creating a model User
class User(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=70, verbose_name='Family name', null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)])
    rating = models.FloatField(default=0.0)
    country = models.CharField(choices=countries, default='DE', verbose_name="Country")


# creating a model UserInfo
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Info")
    married = models.BooleanField(verbose_name="Married?")


# creating a model Actor
class Actor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

# creating a model Director
class Director(models.Model):
    name = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


# creating a model Movie
class Movie(models.Model):
    title = models.CharField(max_length=50)
    actors = models.ManyToManyField(Actor, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, related_name='movies', null=True, blank=True)

    def __str__(self):
        if self.director:
            return f'Title: "{self.title}" | Director: {self.director.name}'
        return f'{self.title}'


class SimpleBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()

    def __str__(self):
        return f'{self.title}'

    def is_classic(self):
        return self.publication_date < 2000

