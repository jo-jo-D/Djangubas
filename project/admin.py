from django.contrib import admin

from project.models import Tag, Dev, Project

class TagAdmin(admin.ModelAdmin):
    # list of the fields to display in the list of model objects
    list_display = ('name',)
    # tasks of the fields to search on
    search_fields = ('name',)



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'lang')
    search_fields = ('name', 'description', 'lang')

class DevAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'projects')
    search_fields = ('name', 'grade', 'projects')

admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Dev, DevAdmin)



