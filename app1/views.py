from django.http import HttpResponse


def hello(request):
    return HttpResponse("Greetings Darina!")

def name_of_pangolin(request):
    return HttpResponse("Son of pangolin - HUGO")