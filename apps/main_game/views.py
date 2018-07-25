from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
import json

def index(request):
    if 'log' not in request.session:
        request.session['log'] = []
    players = request.session['player']
    return render(request, "main_game/index.html", { 'player': Player.objects.get(id=request.session['currPlayer']), 'log': request.session['log'] })
    
def roll_dice(request):
    log = []
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
    player = Player.objects.get(id=request.session['currPlayer'])
    roads = Road.objects.all()
    settlements = Settlement.objects.all()
    settle_dict = {}
    for settlement in settlements:
        settle_dict[settlement.id] = settlement.is_owned()
    road_dict = {}
    for road in roads:
        road_dict[road.id] = road.is_owned()
    context = {
        "player_info": {
            "name": player.name,
            "brick": player.brick,
            "sheep": player.sheep,
            "ore": player.ore,
            "wheat": player.wheat,
            "lumber": player.lumber,
            "vic_points": player.vic_points,
        },
        "log": log,
        "settlements": settle_dict,
        "roads": road_dict
    }
    return JsonResponse(json.dumps(context), safe = False)


def setup(request):
    request.session['currPlayer'] = request.session['player'][0]
    request.session['setup'] = True
    request.session['setup_round'] = 1
    request.session['sett_or_road'] = "settlement"
    print(request.session['setup'])
    return redirect('/game')

def player_turn(request):
    print(request.session['player'])
    print(request.session['currPlayer'])
    for i in range(len(request.session['player'])):
        if request.session['player'][i] == request.session['currPlayer']:
            print('player at i:', request.session['player'][i], 'current player:', request.session['currPlayer'])
            break
    print("i is: ", i)
    if i == len(request.session['player']) - 1:
        request.session['currPlayer'] = request.session['player'][0]
        print('current player is now:', request.session['currPlayer'])
    else:
        i += 1
        request.session['currPlayer'] = request.session['player'][i]
        print('current player is now:', request.session['currPlayer'])
    curr_player = Player.objects.get(id=request.session['currPlayer'])
    context = {
        'player': curr_player
    }
    print("The current player is now "+context['player'].name)
    return render(request, "main_game/info.html", context)

def settlement(request, settlement_id):
    if request.session['setup'] == True:
        if request.session['sett_or_road'] == "settlement":
            return redirect('/setup/setup_settlementr1/'+settlement_id)
        else:
            print("Now is not the time to build a settlement!")
            return render(request, 'main_game/info.html')
    else:
        print("there")
        return redirect('/game/purchase_settlement/'+settlement_id)

def purchase_settlement (request, settlement_id):
    settlement = Settlement.objects.get(id= settlement_id)
    player = Player.objects.get(id=request.session['currPlayer'])
    settlement = Settlement.objects.get(id= int(settlement_id))
    errors = settlement.purchase_settlement(player, False)
    json.dumps([1,2,3])
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
            "player_info": {
                "name": player.name,
                "brick": player.brick,
                "sheep": player.sheep,
                "ore": player.ore,
                "wheat": player.wheat,
                "lumber": player.lumber,
                "vic_points": player.vic_points,
            },
            # "player": player,
            # "roads": roads,
            # "settlements": settlements,
            # "curr_settlement": 5,
            # "player_owned_settlements": Settlement.objects.filter(player=player),
            "success": True
        }
        return render(request, "main_game/info.html", context)
    else:
        request.session['errors'] = errors
        print(*errors)
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        settlement = Settlement.objects.get(id= int(settlement_id))
        context = {
            "player_info": {
                "name": player.name,
                "brick": player.brick,
                "sheep": player.sheep,
                "ore": player.ore,
                "wheat": player.wheat,
                "lumber": player.lumber,
                "vic_points": player.vic_points,
            },
            # "roads": roads.__dict__,
            # "settlements": settlements.__dict__,
            "curr_settlement": 5,
            "success": False
        }
        return JsonResponse(json.dumps(context), safe = False)

def road(request, road_id):
    if request.session['setup'] == True:
        if request.session['sett_or_road'] == "road":
            return redirect('/setup/setup_roadr1/'+road_id)
        else:
            print("Now is not the time to build a road!")
            return render(request, 'main_game/info.html')
    else:
        print("there")
        return redirect('/game/purchase_road/'+road_id)

def purchase_road (request, road_id):
    player = Player.objects.get(id=request.session['currPlayer'])
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
            "player_info": {
                "name": player.name,
                "brick": player.brick,
                "sheep": player.sheep,
                "ore": player.ore,
                "wheat": player.wheat,
                "lumber": player.lumber,
                "vic_points": player.vic_points,
            },
            # "player": player,
            # "roads": roads,
            # "settlements": settlements
            "success": True
        }
        return JsonResponse(json.dumps(context), safe = False)
    else:
        request.session['errors'] = errors
        print(*errors)
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        context = {
            "player_info": {
                "name": player.name,
                "brick": player.brick,
                "sheep": player.sheep,
                "ore": player.ore,
                "wheat": player.wheat,
                "lumber": player.lumber,
                "vic_points": player.vic_points,
            },
            # "player": player,
            # "roads": roads,
            # "settlements": settlements
            "success": False
        }
        return JsonResponse(json.dumps(context), safe = False)

def resources(request):
    player = Player.objects.get(id=request.session['currPlayer'])
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
