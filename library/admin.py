import datetime

from django.contrib import admin
from django import forms
from django.utils import timezone

from library.models import Author, Book, Category, Library, Member, Publisher, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'date_of_birth')
    search_fields = ('name', 'last_name', 'date_of_birth' )


YEAR_CHOICES = [(year, str(year)) for year in range(1900, datetime.date.today().year + 1)]

class BookAdminForm(forms.ModelForm):
    release_year = forms.TypedChoiceField(
        choices=YEAR_CHOICES,
        coerce=int,
        label="Release year"
    )

    class Meta:
        model = Book
        fields = '__all__'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    def update_created_at(self, request, queryset):
        queryset.update(created_at=timezone.now())

    update_created_at.short_description = "Update created_at to current time"

    actions = [update_created_at]

    form = BookAdminForm
    list_display = ('title', 'release_year')
    list_filter = ('release_year',)
    search_fields = ('title',)

# @admin.register(Publisher)
# class PublisherAdmin(admin.ModelAdmin):
#     pass
# не создаю отдельно админ модель паблишера так как мне не нужно отдельно заходить на паблишера а достаточно его создани при добавлении книги


class BookTabu(admin.TabularInline):
    model = Book
    extra = 0

class PublisherAdmin(admin.ModelAdmin):
    inlines = [BookTabu]
admin.site.register(Publisher,
PublisherAdmin)


# class BookInline(admin.StackedInline):
#     model = Book
#     extra = 1

# class PublisherAdmin(admin.ModelAdmin):
#     inlines = [BookInline]
#
# admin.site.register(Publisher, PublisherAdmin)
# admin.site.register(Book)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Library)
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'age')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


