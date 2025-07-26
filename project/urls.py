from project.views import test, list_project, list_task
from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', view=test),
    path('projects/', view=list_project),

]


