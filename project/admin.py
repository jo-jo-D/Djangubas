from django.contrib import admin

from project.models import Tag, Dev, Project, Task

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # list of the fields to display in the list of model objects
    list_display = ('name',)
    # tasks of the fields to search on
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'lang', 'dev')
    search_fields = ('name', 'description', 'lang', 'dev')


@admin.register(Dev)
class DevAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'list_projects')
    search_fields = ('name', 'grade')

    def list_projects(self, obj):
        return ", ".join(p.name for p in obj.projects.all())
    list_projects.short_description = "Projects"


#admin.site.register(Dev, DevAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(Project, ProjectAdmin)


'''     or equal to 
                    ===>
                    
from django.contrib import admin
from project.models import Tag, Dev, Project


@admin.register(Tag, Dev, Project)
class ForAdmin(admin.ModelAdmin):
    pass
    
    
#In the preceding example, the ModelAdmin class doesn’t define any custom values (yet). 
As a result, the default admin interface will be provided. 
If you are happy with the default admin interface, 
you don’t need to define a ModelAdmin object at all – you can register the model class without providing a ModelAdmin description.

                    The preceding example could be simplified to:

from django.contrib import admin
from myapp.models import Author

admin.site.register(Author)                  
                    
                    
                    '''
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project__name', 'status','project','priority', 'updated_at', 'assigned__username')
    list_editable = ('status', 'priority')
    list_filter = ('status', 'priority', 'project', 'assigned__username' )
    read_only_fields = ('created_at',)
    filter_fields = ('status', 'priority', 'project__name', 'due_date', 'created_at')


