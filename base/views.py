from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .form import RoomForm
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

def room_form(request):
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid:
      form.save()
      return redirect('home')
  context = {'form': form }
  return render(request, 'base/room_form.html', context)

  
def update_room(request, pk):
  room = Room.objects.get(id = pk)
  form = RoomForm(instance = room)
  if request.method == 'POST':
    form = RoomForm(request.POST, instance= room)
    if form.is_valid:
      form.save()
      return redirect('home')
  context = {'form': form}
  return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
  room = Room.objects.get(id = pk)
  room.delete()
  return redirect('home') 