from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ZadaniaStale, ZadaniaJednorazowe, PrzydzieloneZadanieStale, H_ZadaniaJednorazowe, H_ZadaniaStale
from .forms import ZadaniaStaleForm, ZadaniaJednorazoweForm, PrzydzieloneZadanieStaleForm, EditJednorazoweForm, EditStaleForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Sum, ExpressionWrapper, F
from django.db import models
import csv
from fpdf import FPDF


def export_to_csv(report_data, filename):
    keys = report_data[0].keys()  # Assuming all dictionaries have the same keys
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(report_data)

def export_to_pdf(report_data, filename):
    class PDF(FPDF):
        def header(self):
            # Add header if needed
            pass

        def footer(self):
            # Add footer if needed
            pass

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    for row in report_data:
        for key, value in row.items():
            pdf.cell(40, 10, str(value), 1)
        pdf.ln()
    pdf.output(filename)

def export_to_html(report_data, filename):
    html = '<table>'
    html += '<tr>'
    for key in report_data[0].keys():
        html += '<th>{}</th>'.format(key)
    html += '</tr>'
    for row in report_data:
        html += '<tr>'
        for value in row.values():
            html += '<td>{}</td>'.format(value)
        html += '</tr>'
    html += '</table>'

    with open(filename, 'w') as html_file:
        html_file.write(html)

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
        prev_started = stale.started
        prev_finished = stale.finished
        form = EditStaleForm(request.POST, instance=stale)
        if form.is_valid():
            h_zadanie = H_ZadaniaStale(
                id_pzs=stale,
                started=prev_started,
                finished=prev_finished
            )
            h_zadanie.save()
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
        prev_started = jednorazowe.started
        prev_finished = jednorazowe.finished
        form = EditJednorazoweForm(request.POST, instance=jednorazowe)
        if form.is_valid():
            # Create a new H_ZadaniaJednorazowe record with the original values
            h_zadanie = H_ZadaniaJednorazowe(
                id_pzs=jednorazowe,
                started=prev_started,
                finished=prev_finished
            )
            h_zadanie.save()
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
            'id': zadanie.id,
            'name': zadanie.name,
            'description': zadanie.description,
            'time_spent': time_spent,
        })

    context = {'report_data': report, 'total_time_spent': total_time_spent}
    return render(request, 'jednorazowy_report.html', context)

# @login_required(login_url='login')
# def generateAllTasks(request):
#     total_time_spent = timedelta()
#     report = []
#     # generating regular tasks
#     stale = ZadaniaStale.objects.all()
#     regular_time_spent = timedelta()
#     for zadanie in stale:
#         assigned_tasks = PrzydzieloneZadanieStale.objects.filter(id_zs=zadanie)
#         if check_group(request.user, "programista"):
#             assigned_tasks = assigned_tasks.filter(recipient=request.user)
#
#         if assigned_tasks.exists():
#             for task in assigned_tasks:
#                 report.append({
#                     'name': task.id_zs.name,
#                     'description': task.id_zs.description,
#                     'recipient': task.recipient,
#                     'created': task.created,
#                     'started': task.started,
#                     'finished': task.finished,
#                     'time': 0 if (task.finished is None or task.started is None) else task.finished - task.created,
#                 })
#
#             completed_tasks = assigned_tasks.exclude(started=None)
#             completed_tasks = completed_tasks.exclude(finished=None)
#             if completed_tasks.exists():
#
#                 regular_time = completed_tasks.aggregate(
#                     total=Sum(ExpressionWrapper(F('finished') - F('created'), output_field=models.DurationField()))
#                 )['total']
#                 if regular_time:
#                     regular_time_spent += regular_time
#
#     # generating singular tasks
#
#     jednorazowe = ZadaniaJednorazowe.objects.filter(
#         Q(started__isnull=False) | Q(finished__isnull=False))
#     if check_group(request.user, "programista"):
#         jednorazowe = jednorazowe.filter(host=request.user)
#
#
#     singular_time_spent = jednorazowe.exclude(started=None, finished=None).aggregate(
#         total=Sum(ExpressionWrapper(F('finished') - F('started'), output_field=models.DurationField()))
#     )['total']
#
#     for zadanie in jednorazowe:
#         time_spent = "Nie ukonczone"
#         if zadanie.started and zadanie.finished:
#             time_spent = zadanie.finished - zadanie.started
#
#         report.append({
#             'name': zadanie.name,
#             'description': zadanie.description,
#             'recipient': zadanie.host,
#             'created': zadanie.created,
#             'started': zadanie.started,
#             'finished': zadanie.finished,
#             'time': time_spent,
#         })
#
#     total_time_spent = regular_time_spent + singular_time_spent
#     context = {'report_data': report, 'total_time_spent': total_time_spent}
#
#     return render(request, 'jednorazowy_report.html', context)

@login_required(login_url='login')
def createEditedDatesReport(request):
    # creating history report of regular tasks
    regular_report = []
    h_regular = H_ZadaniaStale.objects.all()
    for record in h_regular:
        assigned_task = ZadaniaStale.objects.filter(id=record.id_pzs.id_zs.id)
        if assigned_task.exists():
            regular_report.append({
                'id': record,
                'name': record.id_pzs.id_zs.name,
                'description': record.id_pzs.id_zs.description,
                'current_started_date': record.id_pzs.started,
                'history_started_date': record.started,
                'current_finished_date': record.id_pzs.finished,
                'history_finished_date': record.finished,
            })

    # creating history report of singular tasks
    singular_report = []
    h_singular = H_ZadaniaJednorazowe.objects.all()
    for record in h_singular:
        assigned_task = ZadaniaJednorazowe.objects.filter(id=record.id_pzs.id)
        if assigned_task.exists():
            singular_report.append({
                'id': record,
                'name': record.id_pzs.name,
                'description': record.id_pzs.description,
                'current_started_date': record.id_pzs.started,
                'history_started_date': record.started,
                'current_finished_date': record.id_pzs.finished,
                'history_finished_date': record.finished,
            })


    context = {'regular_report': regular_report, 'singular_report': singular_report}
    return render(request, 'edited_dates_report.html', context)

@login_required(login_url='login')
def generateAllTasksReport(request):
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
                    'recipient': task.recipient,
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
        Q(started__isnull=False) | Q(finished__isnull=False))
    if check_group(request.user, "programista"):
        jednorazowe = jednorazowe.filter(host=request.user)


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
            'recipient': zadanie.host,
            'created': zadanie.created,
            'started': zadanie.started,
            'finished': zadanie.finished,
            'time': time_spent,
        })

    total_time_spent = regular_time_spent + singular_time_spent
    context = {'report_data': report, 'total_time_spent': total_time_spent}
    return context
    # return render(request, 'jednorazowy_report.html', context)

@login_required(login_url='login')
def generateSpecificTasks(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        return redirect('generate-user-tasks-report', user_id=user_id)

    context = {
        'users': User.objects.filter(groups__name='programista')
    }
    return render(request, 'select_user_specific.html', context)


@login_required(login_url='login')
def generateUserTasksReport(request, user_id):
    user = get_object_or_404(User, id=user_id)
    total_time_spent = timedelta()
    report = []

    # Generating regular tasks
    stale = ZadaniaStale.objects.all()
    regular_time_spent = timedelta()
    for zadanie in stale:
        assigned_tasks = PrzydzieloneZadanieStale.objects.filter(id_zs=zadanie, recipient=user)

        if assigned_tasks.exists():
            for task in assigned_tasks:
                report.append({
                    'type': 'Zadanie Stałe',
                    'name': task.id_zs.name,
                    'description': task.id_zs.description,
                    'recipient': task.recipient,
                    'created': task.created,
                    'started': task.started,
                    'finished': task.finished,
                    'time': 0 if (task.finished is None or task.started is None) else task.finished - task.created,
                })

            completed_tasks = assigned_tasks.exclude(started=None).exclude(finished=None)
            if completed_tasks.exists():
                regular_time = completed_tasks.aggregate(
                    total=Sum(ExpressionWrapper(F('finished') - F('created'), output_field=models.DurationField()))
                )['total']
                if regular_time:
                    regular_time_spent += regular_time

    # Generating singular tasks
    jednorazowe = ZadaniaJednorazowe.objects.filter(Q(started__isnull=False) | Q(finished__isnull=False), host=user)

    singular_time_spent = timedelta()
    singular_time_spent = jednorazowe.exclude(started=None, finished=None).aggregate(
        total=Sum(ExpressionWrapper(F('finished') - F('started'), output_field=models.DurationField()))
    )['total']

    if singular_time_spent is None:
        singular_time_spent = timedelta()

    for zadanie in jednorazowe:
        time_spent = "Nie ukonczone"
        if zadanie.started and zadanie.finished:
            time_spent = zadanie.finished - zadanie.started

        report.append({
            'type': 'Zadanie Jednorazowe',
            'name': zadanie.name,
            'description': zadanie.description,
            'recipient': zadanie.host,
            'created': zadanie.created,
            'started': zadanie.started,
            'finished': zadanie.finished,
            'time': time_spent,
        })

    total_time_spent = timedelta()
    total_time_spent = regular_time_spent + singular_time_spent

    context = {
        'report_data': report,
        'total_time_spent': total_time_spent,
        'user': user,
        'extract_available': True,
    }
    return context

def showGeneratedUserTasksReport(request, user_id):
    context = generateUserTasksReport(request, user_id)
    return render(request, 'user_tasks_report.html', context)

@login_required(login_url='login')
def exportUserTasksReportCSV(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = generateUserTasksReport(request, user_id)
    filename = 'user_' + user.name + '_tasks_report.csv'
    export_to_csv(context['report_data'], filename)
    return render(request, 'user_tasks_report.html', context)

@login_required(login_url='login')
def exportUserTasksReportPDF(request, user_id):
    context = generateUserTasksReport(request, user_id)
    export_to_pdf(context['report_data'], 'report.pdf')
    return render(request, 'user_tasks_report.html', context)

@login_required(login_url='login')
def exportUserTasksReportHTML(request, user_id):
    context = generateUserTasksReport(request, user_id)
    export_to_html(context['report_data'], 'report.html')
    return render(request, 'user_tasks_report.html', context)