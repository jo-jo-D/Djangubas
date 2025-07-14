from django.contrib import admin
from app1.models import User, UserInfo, Actor, Movie, Director

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'age', 'rating', 'country')
    search_fields = ('name', 'last_name', 'age', 'rating', 'country')

    def set_rating_to_0(self, request, queryset):
        queryset.update(rating=0.0)

    set_rating_to_0.short_description = "Set user's rating to null"

    actions = [set_rating_to_0]

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display=('user', 'married')
    search_fields = ('user', 'married')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)


#admin.py

class MovieInline(admin.TabularInline):
    model = Movie
    extra = 2

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    inlines = [MovieInline]