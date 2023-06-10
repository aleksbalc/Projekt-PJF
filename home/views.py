from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ZadaniaStale, ZadaniaJednorazowe
from .forms import ZadaniaStaleForm, ZadaniaJednorazoweForm
from django.contrib.auth.models import User, Group
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


@login_required(login_url='login')
def home(request):
    stales = ZadaniaStale.objects.all()
    user = User.objects.get(username=request.user.username)
    is_kierownik = check_group(user, "kierownik")
    is_programista = check_group(user, "programista")

    context = {'stales': stales, 'is_kierownik': is_kierownik, 'is_programista':is_programista}
    return render(request, 'home.html', context)

def check_group(user, name):
    # Check if the user belongs to the str group
    is_in_group = user.groups.filter(name=name).exists()
    return is_in_group

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

