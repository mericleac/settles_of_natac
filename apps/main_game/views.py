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

def purchase_settlement (request, settlement_id):
    # replace with current player
    player = Player.objects.last()
    settlement = Settlement.objects.get(id= int(settlement_id))
    errors = settlement.purchase_settlement(player, False)
    if len(errors) == 0:
        player.brick -= 1
        player.lumber -= 1
        player.sheep -= 1
        player.wheat -= 1
        player.vic_points += 1
        player.save()
        settlement.player = player
        settlement.save()
        return redirect('/game')
    else:
        request.session['errors'] = errors
        print(*errors)
        return redirect('/game')

def purchase_road (request, road_id):
    # replace with current player
    player = Player.objects.last()
    road = Road.objects.get(id = int(road_id))
    print("*" * 100)
    print(road)
    print(road.player)
    errors = road.purchase_road(player)
    if len(errors) == 0:
        player.brick -= 1
        player.lumber -= 1
        player.save()
        road.player = player
        road.save()
        return redirect('/game')
    else:
        request.session['errors'] = errors
        print(*errors)
        return redirect('/game')
        



