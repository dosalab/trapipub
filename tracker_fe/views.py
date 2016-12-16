from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template=loader.get_template('tracker_fe/index.html')
    context={'message':"Hello, world. You are at the tracking system now"}
    return render(request,'tracker_fe/index.html',context)

    
