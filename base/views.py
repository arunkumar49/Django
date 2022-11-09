from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.

# rooms = [
#   {'id': 1, 'name':'Lets learn python.'},
#   {'id': 2, 'name':'Lets learn django.'},
#   {'id': 3, 'name':'Lets learn web development.'}
# ]

def home(request):
  rooms = Room.objects.all()
  return render(request, 'base/home.html', {'room': rooms})

def room(request,pk):
  room = Room.objects.get(id = pk)
  context = {'room': room}
  return render(request, 'base/room.html', context)
    
  
