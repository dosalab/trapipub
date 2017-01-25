from django.shortcuts import render

def index(request):
    context = {'message':"Hello, world. You are at the tracking system now"}
    return render(request, 'tracker_fe/welcome.html', context)
