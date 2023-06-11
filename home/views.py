from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ZadaniaStale, ZadaniaJednorazowe, PrzydzieloneZadanieStale, H_ZadaniaJednorazowe, H_ZadaniaStale
from .forms import ZadaniaStaleForm, ZadaniaJednorazoweForm, PrzydzieloneZadanieStaleForm, EditJednorazoweForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Sum, ExpressionWrapper, F
from django.db import models


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
    jednorazowes = ZadaniaJednorazowe.objects.all()
    p_stales = PrzydzieloneZadanieStale.objects.all()
    user = User.objects.get(username=request.user.username)
    is_kierownik = check_group(user, "kierownik")
    is_programista = check_group(user, "programista")
    context = {'stales': stales, 'jednorazowes': jednorazowes, 'p_stales': p_stales, 'is_kierownik': is_kierownik, 'is_programista':is_programista}
    return render(request, 'home.html', context)

def check_group(user, name):
    # Check if the user belongs to the str group
    is_in_group = user.groups.filter(name=name).exists()
    return is_in_group

def stale(request, pk):
    stale = ZadaniaStale.objects.get(id=pk)
    context = {'stale': stale}
    return render(request, 'stale.html', context)

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
def createPrzydzieloneStale(request):
    form = PrzydzieloneZadanieStaleForm()
    if request.method == 'POST':
        form = PrzydzieloneZadanieStaleForm(request.POST)
        if form.is_valid():
            przydzielone_zadanie_stale = form.save(commit=False)
            przydzielone_zadanie_stale.host = request.user
            przydzielone_zadanie_stale.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'stale_form.html', context)

@login_required(login_url='login')
def startStale(request, pk):
    task = PrzydzieloneZadanieStale.objects.get(id=pk)
    # Assign the current system date to the 'started' column
    task.started = timezone.now()
    task.save()

    return redirect('home')

@login_required(login_url='login')
def finishStale(request, pk):
    task = PrzydzieloneZadanieStale.objects.get(id=pk)
    # Assign the current system date to the 'started' column
    task.finished = timezone.now()
    task.save()

    return redirect('home')

@login_required(login_url='login')
def editStale(request, pk):
    stale = PrzydzieloneZadanieStale.objects.get(id=pk)
    form = EditJednorazoweForm(instance=stale)

    if request.method == 'POST':
        form = EditJednorazoweForm(request.POST, instance=stale)
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
def startJednorazowe(request, pk):
    task = ZadaniaJednorazowe.objects.get(id=pk)
    # Assign the current system date to the 'started' column
    task.started = timezone.now()
    task.save()

    return redirect('home')

@login_required(login_url='login')
def finishJednorazowe(request, pk):
    task = ZadaniaJednorazowe.objects.get(id=pk)
    # Assign the current system date to the 'finished' column
    task.finished = timezone.now()
    task.save()

    return redirect('home')

@login_required(login_url='login')
def editJednorazowe(request, pk):
    jednorazowe = ZadaniaJednorazowe.objects.get(id=pk)
    form = EditJednorazoweForm(instance=jednorazowe)

    if request.method == 'POST':
        form = EditJednorazoweForm(request.POST, instance=jednorazowe)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'jednorazowe_form.html', context)

@login_required(login_url='login')
def generateStaly(request):
    stale = ZadaniaStale.objects.all()

    report = []
    total_time_spent = timedelta()
    for zadanie in stale:
        assigned_tasks = PrzydzieloneZadanieStale.objects.filter(id_zs=zadanie)
        if check_group(request.user, "programista"):
            assigned_tasks = assigned_tasks.filter(recipient=request.user)

        if assigned_tasks.exists():
            for task in assigned_tasks:
                report.append({
                    'name': task.id_zs.name,
                    'description': task.id_zs.description,
                    'created': task.created,
                    'started': task.started,
                    'finished': task.finished,
                    'time': 0 if (task.finished is None or task.started is None) else task.finished - task.created,
                })

            completed_tasks = assigned_tasks.exclude(started=None)
            completed_tasks = completed_tasks.exclude(finished=None)
            if completed_tasks.exists():

                total_time = completed_tasks.aggregate(
                    total=Sum(ExpressionWrapper(F('finished') - F('created'), output_field=models.DurationField()))
                )['total']
                if total_time:
                    total_time_spent += total_time

    context = {'report_data': report, 'total_time_spent': total_time_spent}
    return render(request, 'jednorazowy_report.html', context)

@login_required(login_url='login')
def generateJednorazowy(request):
    jednorazowe = ZadaniaJednorazowe.objects.filter(
    Q(started__isnull=False) | Q(finished__isnull=False),
    host=request.user)

    total_time_spent = jednorazowe.exclude(started=None, finished=None).aggregate(
        total=Sum(ExpressionWrapper(F('finished') - F('started'), output_field=models.DurationField()))
    )['total']

    report = []
    for zadanie in jednorazowe:
        time_spent = "Nie ukonczone"
        if zadanie.started and zadanie.finished:
            time_spent = zadanie.finished - zadanie.started

        report.append({
            'name': zadanie.name,
            'description': zadanie.description,
            'created': zadanie.created,
            'started': zadanie.started,
            'finished': zadanie.finished,
            'time': time_spent,
        })


    context = {'report_data': report, 'total_time_spent': total_time_spent}
    return render(request, 'jednorazowy_report.html', context)

@login_required(login_url='login')
def generateAllTasks(request):
    total_time_spent = timedelta()
    report = []
    # generating regular tasks
    stale = ZadaniaStale.objects.all()
    regular_time_spent = timedelta()
    for zadanie in stale:
        assigned_tasks = PrzydzieloneZadanieStale.objects.filter(id_zs=zadanie)
        if check_group(request.user, "programista"):
            assigned_tasks = assigned_tasks.filter(recipient=request.user)

        if assigned_tasks.exists():
            for task in assigned_tasks:
                report.append({
                    'name': task.id_zs.name,
                    'description': task.id_zs.description,
                    'created': task.created,
                    'started': task.started,
                    'finished': task.finished,
                    'time': 0 if (task.finished is None or task.started is None) else task.finished - task.created,
                })

            completed_tasks = assigned_tasks.exclude(started=None)
            completed_tasks = completed_tasks.exclude(finished=None)
            if completed_tasks.exists():

                regular_time = completed_tasks.aggregate(
                    total=Sum(ExpressionWrapper(F('finished') - F('created'), output_field=models.DurationField()))
                )['total']
                if regular_time:
                    regular_time_spent += regular_time

    # generating singular tasks

    jednorazowe = ZadaniaJednorazowe.objects.filter(
        Q(started__isnull=False) | Q(finished__isnull=False),
        host=request.user)

    singular_time_spent = jednorazowe.exclude(started=None, finished=None).aggregate(
        total=Sum(ExpressionWrapper(F('finished') - F('started'), output_field=models.DurationField()))
    )['total']

    for zadanie in jednorazowe:
        time_spent = "Nie ukonczone"
        if zadanie.started and zadanie.finished:
            time_spent = zadanie.finished - zadanie.started

        report.append({
            'name': zadanie.name,
            'description': zadanie.description,
            'created': zadanie.created,
            'started': zadanie.started,
            'finished': zadanie.finished,
            'time': time_spent,
        })

    total_time_spent = regular_time_spent + singular_time_spent
    context = {'report_data': report, 'total_time_spent': total_time_spent}
    return render(request, 'jednorazowy_report.html', context)
