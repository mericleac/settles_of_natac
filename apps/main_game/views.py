from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    if 'log' not in request.session:
        request.session['log'] = []
    return render(request, "main_game/index.html", { 'player': Player.objects.last(), 'log': request.session['log'] })

def roll_dice(request):
    log = request.session['log']
    from random import randint
    die1 = randint(1, 6)
    log.append('first dice was: ' + str(die1))
    die2 = randint(1, 6)
    log.append('second dice was: ' + str(die2))
    log.append('total was: ' + str(die1 + die2))
    rolled = Field.objects.filter(number=die1 + die2)
    if len(rolled) == 0:
        log.append('no field matched the roll')
    else:
        for field in rolled:
            log.append('alloting resources for: ' + str(field.number) + " " + field.resource)
            messages = field.distribute_resources()
            if messages:
                log.append(*messages)
    request.session['log'] = log
    return redirect('/game')