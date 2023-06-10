from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, ZadaniaStale, ZadaniaJednorazowe
from .forms import RoomForm, ZadaniaStaleForm, ZadaniaJednorazoweForm
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
    jednorazowes = ZadaniaJednorazowe.objects.all()
    context = {'stales': stales, 'jednorazowes': jednorazowes}
    return render(request, 'home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'room.html', context)

def stale(request, pk):
    stale = ZadaniaStale.objects.get(id=pk)
    context = {'stale': stale}
    return render(request, 'stale.html', context)

def jednorazowe(request, pk):
    jednorazowe = ZadaniaJednorazowe.objects.get(id=pk)
    context = {'jednorazowe': jednorazowe}
    return render(request, 'jednorazowe.html', context)


@login_required(login_url='login')
def createStale(request):
    form = ZadaniaStaleForm()
    if request.method == 'POST':
        form = ZadaniaStaleForm(request.POST)
        if form.is_valid():
            zadanie_stale = form.save(commit=False)
            zadanie_stale.host = request.user
            zadanie_stale.save()
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
def createJednorazowe(request):
    form = ZadaniaJednorazoweForm()
    if request.method == 'POST':
        form = ZadaniaJednorazoweForm(request.POST)
        if form.is_valid():
            zadanie_jednorazowe = form.save(commit=False)
            zadanie_jednorazowe.host = request.user
            zadanie_jednorazowe.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'jednorazowe_form.html', context)

@login_required(login_url='login')
def updateJednorazowe(request, pk):
    jednorazowe = ZadaniaJednorazowe.objects.get(id=pk)
    form = ZadaniaJednorazoweForm(instance=jednorazowe)

    if request.user != jednorazowe.host:
        return HttpResponse("You cant do that")

    if request.method == 'POST':
        form = ZadaniaJednorazoweForm(request.POST, instance=jednorazowe)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'jednorazowe_form.html', context)


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