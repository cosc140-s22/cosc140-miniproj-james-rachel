from django.shortcuts import render

def index(request):
    print("here")
    return render(request, 'castles/index.html')
