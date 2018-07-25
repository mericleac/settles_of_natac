from django.shortcuts import render, HttpResponse, redirect
from .models import *
import json

def index(request):
    if 'log' not in request.session:
        request.session['log'] = []
    return render(request, "main_game/index.html", { 'player': Player.objects.last(), 'log': request.session['log'] })

def roll_dice(request):
    log = request.session['log']
    print(log)
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
                for message in messages:
                    log.append(message)
    request.session['log'] = log
    player = Player.objects.last()
    roads = Road.objects.all()
    settlements = Settlement.objects.all()
    context = {
        "player": player,
        "roads": roads,
        "settlements": settlements
    }
    return render(request, "main_game/circle.html", context)


def setup(request):
    request.session['currPlayer'] = request.session['player'][0]
    return redirect('/game/player_turn')

def player_turn(request):
    print(request.session['player'])
    print(request.session['currPlayer'])
    for i in range(len(request.session['player'])):
        if request.session['player'][i] == request.session['currPlayer']:
            #print('player at i:', request.session['player'][i], 'current player:', request.session['currPlayer'])
            break
    #print("i is: ", i)
    if i == len(request.session['player']) - 1:
        request.session['currPlayer'] = request.session['player'][0]
        #print('current player is now:', request.session['currPlayer'])
    else:
        i += 1
        request.session['currPlayer'] = request.session['player'][i]
        #print('current player is now:', request.session['currPlayer'])
    return redirect('/game')

def purchase_settlement (request, settlement_id):
    # replace with current player
    settlement = Settlement.objects.get(id= settlement_id)
    player = Player.objects.last()
    settlement = Settlement.objects.get(id= int(settlement_id))
    curr_settlement = settlement.id
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
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        context = {
            "player": player,
            "roads": roads,
            "settlements": settlements,
            "curr_settlement": 5
        }
        return render(request, "main_game/circle.html", context)
    else:
        request.session['errors'] = errors
        print(*errors)
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        settlement = Settlement.objects.get(id= int(settlement_id))
        context = {
            "player": player,
            "roads": roads,
            "settlements": settlements,
            "curr_settlement": 5
        }
        return render(request, "main_game/circle.html", context)

def purchase_road (request, road_id):
    # replace with current player
    player = Player.objects.last()
    road = Road.objects.get(id = int(road_id))
    errors = road.purchase_road(player)
    print(errors)
    if len(errors) == 0:
        player.brick -= 1
        player.lumber -= 1
        player.save()
        road.player = player
        road.save()
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        context = {
            "player": player,
            "roads": roads,
            "settlements": settlements
        }
        return render(request, "main_game/circle.html", context)
    else:
        request.session['errors'] = errors
        print(*errors)
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        context = {
            "player": player,
            "roads": roads,
            "settlements": settlements
        }
        return render(request, "main_game/circle.html", context)

def resources(request):
    player = Player.objects.last()
    player.brick = 20
    player.wheat = 20
    player.ore = 20
    player.sheep = 20
    player.lumber = 20
    player.save()
    return redirect("/game")

def clear(request):
    roads = Road.objects.all()
    settlements = Settlement.objects.all()
    for road in roads:
        road.player = None
        road.save()
    for settlement in settlements:
        settlement.player = None
        settlement.save()
    return redirect("/game")
