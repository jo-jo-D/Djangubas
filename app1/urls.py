from app1.views import hello, name_of_pangolin
from django.urls import path


urlpatterns = [path("hello/", view=hello, name="greeting"),
               path('filsdepute/', name_of_pangolin),
               ]

# from django.urls import path
# from . import views
# urlpatterns = [path("name/", views.hello_world, name="hello_world")]