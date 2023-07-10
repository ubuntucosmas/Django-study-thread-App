from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q       #this is the Q lookup method that allows us to add in statements like 'or' 'and' into the search
from .models import Room, Topic, Message
from .forms import RoomForm



# rooms=[
#     {'id':1, 'name':'lets learn python!'},
#     {'id':2, 'name':'Design with me!'},
#     {'id':3, 'name':'Frontend developers!'},
# ]
# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST': # getting the user credentials
        username = request.POST.get('username').lower()
        password = request.POST.get('password')  
        try:
            user = User.objects.get(username=username)  #checking if the user exist
        except:
             messages.error(request, 'user does not exist') #does not exist through an eror message

        user = authenticate(request, username=username, password=password) #==> user authentication---this will return back
        #a user object that matches these credentials
        if user is not None:
            login(request, user)   # this creates a session in the DB & browser
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist!')

    context={ 'page':page}

    return render(request, 'webflow/login_register.html', context)

def logoutUser(request):
    logout(request) # this method deletes session token in the db and browser hence loging out the user
    return redirect('home')



def registerPage(request):
    page = 'register'   # checking if th epage is login the we render out the login form
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST) #passing in the data
        if form.is_valid():
            user = form.save(commit=False) #commit false so that we can be able to access the user right away
            user.username = user.username.lower() 
            user.save()
            login(request, user) #user is logged in after registering
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!')

    context = {'form': form}
    return render(request, 'webflow/login_register.html', context)



def home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else  ''  #search by topic logic
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |    #  '|'==> means OR
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )  
    #now we can search topic-name, roomm-name and description^
    #objects is a model manager that helps in making queries by going into the models
    # all() gives us all the rooms in the database
    topics = Topic.objects.all()
    room_count = rooms.count()   # or in python we can use  room_count= rooms.len()
    room_messages = Message.objects.all().order_by('-created')
    context = {'rooms':rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages}  #   ==>   then we use the context variable to pass the list to the render method
    return render(request, 'webflow/home.html', context)



def room(request, pk): # pk is a dynamic value that can be typed on the url
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') #quering is child object of a specific room, {message_set} message=model name and a set of all messages
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body') # geting the message body from the coment form with name='body'
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants':participants}

    return render(request, 'webflow/room.html',context)


@login_required(login_url='login') # this is a decorator that redirects the user to the login page if the user is trying to create a room and yet the user is not logged in
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)  #passing in all the post data into the form and the form already know what data to extract from there
        if form.is_valid():
            form.save()
            return redirect('home') #sending the user back to the homepage [home=url name]
        
    context = {'form': form}
    return render(request, 'webflow/room_form.html', context)


@login_required(login_url='login')     #decorators
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # this room is pre-filled with the above room values
    if request.user != room.host:
        return HttpResponse('You are not allowed to update the room')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) # we specify which room to update
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'webflow/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed to update the room')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'webflow/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'webflow/delete.html', context)




    # USER PROFILE VIEW

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    context={'user':user, 'rooms': rooms}
    return render(request, 'webflow/profile.html', context)