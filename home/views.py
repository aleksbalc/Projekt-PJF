from django.shortcuts import render

# Create your views here.

rooms = [
    {'id': 1, 'name': "Stale zadania"},
    {'id': 2, 'name': "Jednorazowe zadania"},
    {'id': 3, 'name': "Kalendarz zadan"},
    {'id': 4, 'name': "Generowanie raportow"},
    {'id': 5, 'name': "Eksport raportow"},
]

def home(request):
    return render(request, 'home.html', {'rooms':rooms})

def room(request):
    return render(request, 'room.html')