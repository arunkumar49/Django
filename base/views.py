from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Room, Topic, Message
from django.contrib.auth.models import User
from . form import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 


# Create your views here.

def login_reg(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    try:
      user = User.objects.get(username = username)
    except:
      messages.error(request, 'Username does not exist.')
      
    user = authenticate(request, username = username, password = password)
    
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username or Password is not correct.')
      
  context = {'page': page}
  return render(request, 'base/login.html', context)



def registerPage(request):
  form = UserCreationForm()
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user  = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'An error occured while regiestering')
  context = {'form': form }
  return render(request, 'base/login.html', context)



def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(description__icontains=q) |
    Q(name__icontains=q) |
    Q(host__username__icontains = q)
  )
  topics = Topic.objects.all()
  context = {'room': rooms, 'topics': topics}
  return render(request, 'base/home.html', context)



def room(request, pk):
  room = Room.objects.get(id=pk)
  messages = room.message_set.all()
  
  if request.method == 'POST':
    message = Message.objects.create(
      user = request.user,
      room = room,
      body = request.POST.get('body')
    )
    return redirect('room', pk = room.id)
  
  context = {'room': room, 'messages': messages}
  return render(request, 'base/room.html', context)



@login_required(login_url='login_reg')
def room_form(request):                     #Function for creating new room
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid:
      form.save()
      return redirect('home')
  context = {'form': form}
  return render(request, 'base/room_form.html', context)



@login_required(login_url='login_reg')
def update_room(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  
  if request.user != room.host:
    return HttpResponse("You are not allowed to this page.")
  
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid:
      form.save()
      return redirect('home')
  context = {'form': form}
  return render(request, 'base/room_form.html', context)



@login_required(login_url='login_reg')
def delete_room(request, pk):
  room = Room.objects.get(id=pk)
  if request.user != room.host:
    return HttpResponse("You are not allowed to delete others room.")
  if request.method == 'GET':
    room.delete()
  return redirect('home')



def logout_view(request):
  logout(request)
  return redirect('home')