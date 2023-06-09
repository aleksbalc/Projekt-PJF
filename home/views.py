from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, ZadaniaStale
from .forms import RoomForm, ZadaniaStaleForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    context = {}
    return render(request, 'login_registration.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    stales = ZadaniaStale.objects.all()
    context = {'stales': stales}
    return render(request, 'home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'room.html', context)


@login_required(login_url='login')
def createStale(request):
    form = ZadaniaStaleForm()
    if request.method == 'POST':
        form = ZadaniaStaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'stale_form.html', context)

@login_required(login_url='login')
def updateStale(request, pk):
    stale = ZadaniaStale.objects.get(id=pk)
    form = ZadaniaStaleForm(instance=stale)

    if request.user != stale.recipients:
        return HttpResponse("You cant do that")

    if request.method == 'POST':
        form = ZadaniaStaleForm(request.POST, instance=stale)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'stale_form.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You cant do that")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room_form.html', context)