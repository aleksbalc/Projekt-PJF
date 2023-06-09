from django.shortcuts import render
from .models import Room

# Create your views here.

#rooms = [
#    {'id': 1, 'name': "Stale zadania"},
#    {'id': 2, 'name': "Jednorazowe zadania"},
#    {'id': 3, 'name': "Kalendarz zadan"},
#    {'id': 4, 'name': "Generowanie raportow"},
#    {'id': 5, 'name': "Eksport raportow"},
#]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'room.html', context)