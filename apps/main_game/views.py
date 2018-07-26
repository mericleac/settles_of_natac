from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
import json

def index(request):
    if 'log' not in request.session:
        request.session['log'] = []
    players = request.session['player']
    return render(request, "main_game/index.html", { 'player': Player.objects.get(id=request.session['currPlayer']), 'log': request.session['log']})
    
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
        "roads": road_dict,
    }
    return JsonResponse(json.dumps(context), safe = False)


def setup(request):
    request.session['currPlayer'] = request.session['player'][0]
    request.session['setup'] = True
    request.session['setup_round'] = 1
    request.session['sett_or_road'] = "settlement"
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
        i = 0
        request.session['currPlayer'] = request.session['player'][i]
        print('current player is now:', request.session['currPlayer'])
    else:
        i += 1
        request.session['currPlayer'] = request.session['player'][i]
        print('current player is now:', request.session['currPlayer'])
    curr_player = Player.objects.get(id=request.session['currPlayer'])
    request.session['player_index'] = i
    all_players = []
    for player in request.session['player']:
        all_players.append(Player.objects.get(id=player))
    context = {
        "player_info": {
            "name": curr_player.name,
            "brick": curr_player.brick,
            "sheep": curr_player.sheep,
            "ore": curr_player.ore,
            "wheat": curr_player.wheat,
            "lumber": curr_player.lumber,
            "vic_points": curr_player.vic_points,
        },
        "curr_player": i,
        'players':all_players,
        'currPlayer':curr_player,
    }
    print("The current player is now "+ context['player_info']['name'])
    print("currPlayer is:", curr_player.name)
    return render(request, "main_game/partners.html", context)

def settlement(request, settlement_id):
    #request.session['setup'] = False
    if request.session['setup'] == True:
        if request.session['sett_or_road'] == "settlement":
            return redirect('/setup/setup_settlementr1/'+settlement_id)
        else:
            print("Now is not the time to build a settlement!")
            curr_player = Player.objects.get(id=request.session['currPlayer'])
            context = {
                "player_info": {
                    "name": curr_player.name,
                    "brick": curr_player.brick,
                    "sheep": curr_player.sheep,
                    "ore": curr_player.ore,
                    "wheat": curr_player.wheat,
                    "lumber": curr_player.lumber,
                    "vic_points": curr_player.vic_points,
                },
                "success": False,
                "errors": ["Now is not the time to build a settlement!"]
            }
            return JsonResponse(json.dumps(context), safe = False)
    else:
        print("there")
        return redirect('/game/purchase_settlement/'+settlement_id)

def purchase_settlement (request, settlement_id):
    settlement = Settlement.objects.get(id= settlement_id)
    player = Player.objects.get(id=request.session['currPlayer'])
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
            "success": True
        }
        return JsonResponse(json.dumps(context), safe = False)
    else:
        request.session['errors'] = errors
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
            "errors": errors,
            "success": False
        }
        return JsonResponse(json.dumps(context), safe = False)

def road(request, road_id):
    request.session['setup'] == False
    if request.session['setup'] == True:
        if request.session['sett_or_road'] == "road":
            return redirect('/setup/setup_roadr1/'+road_id)
        else:
            curr_player = Player.objects.get(id=request.session['currPlayer'])
            context = {
                "player_info": {
                    "name": curr_player.name,
                    "brick": curr_player.brick,
                    "sheep": curr_player.sheep,
                    "ore": curr_player.ore,
                    "wheat": curr_player.wheat,
                    "lumber": curr_player.lumber,
                    "vic_points": curr_player.vic_points,
                },
                "success": False,
                "errors": ["Now is not the time to build a road!"]
            }
            print("Now is not the time to build a road!")
            return JsonResponse(json.dumps(context), safe = False)
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
            'errors': errors,
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
    players = Player.objects.all()
    for road in roads:
        road.player = None
        road.save()
    for settlement in settlements:
        settlement.player = None
        settlement.save()
    for player in players:
        player.vic_points = 0
        player.save()
    return redirect("/game")

def initialize_db(request):
    Field.objects.create(resource = 'lumber', robber=False, number = 11)
    Field.objects.create(resource = 'sheep', robber=False, number = 12)
    Field.objects.create(resource = 'wheat', robber=False, number = 9)
    Field.objects.create(resource = 'brick', robber=False, number = 4)
    Field.objects.create(resource = 'ore', robber=False, number = 6)
    Field.objects.create(resource = 'brick', robber=False, number = 5)
    Field.objects.create(resource = 'sheep', robber=False, number = 10)
    Field.objects.create(resource = 'lumber', robber=False, number = 3)
    Field.objects.create(resource = 'wheat', robber=False, number = 11)
    Field.objects.create(resource = 'lumber', robber=False, number = 4)
    Field.objects.create(resource = 'wheat', robber=False, number = 8)
    Field.objects.create(resource = 'brick', robber=False, number = 8)
    Field.objects.create(resource = 'sheep', robber=False, number = 10)
    Field.objects.create(resource = 'sheep', robber=False, number = 9)
    Field.objects.create(resource = 'ore', robber=False, number = 3)
    Field.objects.create(resource = 'ore', robber=False, number = 5)
    Field.objects.create(resource = 'wheat', robber=False, number = 2)
    Field.objects.create(resource = 'lumber', robber=False, number = 6)
    for i in range (1, 73):
        Road.objects.create()
    for i in range (1, 4):
        Settlement.objects.create()
    for i in range (1, 55):
        Settlement.objects.create()
    for i in range (1, 7):
        R = Road.objects.get(id=i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i+3)))
        R.save()
        R.adjacent_settlements.add(Settlement.objects.get(id = (i+4)))
        R.save()
    for i in range (11, 19):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = i))
        R.save()
        R.adjacent_settlements.add(Settlement.objects.get(id = (i+1)))
        R.save()
    for i in range(23, 34):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-4)))
        R.save()
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-3)))
        R.save()
    for i in range(41, 50):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 10)))
        R.save()
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 9)))
        R.save()
    for i in range(55, 63):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 14)))
        R.save()
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 13)))
    for i in range(67, 73):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-17)))
        R.save()
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-16)))
        R.save()
    R = Road.objects.get(id = 7)
    R.adjacent_settlements.add(Settlement.objects.get(id = 4))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 12))
    R.save()
    R = Road.objects.get(id = 8)
    R.adjacent_settlements.add(Settlement.objects.get(id = 6))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 14))
    R.save()
    R = Road.objects.get(id = 9)
    R.adjacent_settlements.add(Settlement.objects.get(id = 8))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 16))
    R.save()
    R = Road.objects.get(id = 10)
    R.adjacent_settlements.add(Settlement.objects.get(id = 10))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 18))
    R.save()
    R = Road.objects.get(id = 19)
    R.adjacent_settlements.add(Settlement.objects.get(id = 11))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 21))
    R.save()
    R = Road.objects.get(id = 20)
    R.adjacent_settlements.add(Settlement.objects.get(id = 13))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 23))
    R.save()
    R = Road.objects.get(id = 21)
    R.adjacent_settlements.add(Settlement.objects.get(id = 15))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 25))
    R.save()
    R = Road.objects.get(id = 22)
    R.adjacent_settlements.add(Settlement.objects.get(id = 17))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 27))
    R.save()
    R = Road.objects.get(id = 34)
    R.adjacent_settlements.add(Settlement.objects.get(id = 20))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 57))
    R.save()
    R = Road.objects.get(id = 35)
    R.adjacent_settlements.add(Settlement.objects.get(id = 22))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 32))
    R.save()
    R = Road.objects.get(id = 36)
    R.adjacent_settlements.add(Settlement.objects.get(id = 24))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 34))
    R.save()
    R = Road.objects.get(id = 37)
    R.adjacent_settlements.add(Settlement.objects.get(id = 26))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 36))
    R.save()
    R = Road.objects.get(id = 38)
    R.adjacent_settlements.add(Settlement.objects.get(id = 28))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 38))
    R.save()
    R = Road.objects.get(id = 39)
    R.adjacent_settlements.add(Settlement.objects.get(id = 30))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 40))
    R.save()
    R = Road.objects.get(id = 40)
    R.adjacent_settlements.add(Settlement.objects.get(id = 31))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 57))
    R.save()
    R = Road.objects.get(id = 50)
    R.adjacent_settlements.add(Settlement.objects.get(id = 31))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 41))
    R.save()
    R = Road.objects.get(id = 51)
    R.adjacent_settlements.add(Settlement.objects.get(id = 33))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 43))
    R.save()
    R = Road.objects.get(id = 52)
    R.adjacent_settlements.add(Settlement.objects.get(id = 35))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 45))
    R.save()
    R = Road.objects.get(id = 53)
    R.adjacent_settlements.add(Settlement.objects.get(id = 37))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 47))
    R.save()
    R = Road.objects.get(id = 54)
    R.adjacent_settlements.add(Settlement.objects.get(id = 39))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 49))
    R.save()
    R = Road.objects.get(id = 63)
    R.adjacent_settlements.add(Settlement.objects.get(id = 42))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 50))
    R.save()
    R = Road.objects.get(id = 64)
    R.adjacent_settlements.add(Settlement.objects.get(id = 44))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 52))
    R.save()
    R = Road.objects.get(id = 65)
    R.adjacent_settlements.add(Settlement.objects.get(id = 46))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 54))
    R.save()
    R = Road.objects.get(id = 66)
    R.adjacent_settlements.add(Settlement.objects.get(id = 48))
    R.save()
    R.adjacent_settlements.add(Settlement.objects.get(id = 56))
    R.save()
    S = Settlement.objects.get(id = 4)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 5)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 6)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 6)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 7)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 8)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 8)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 9)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 10)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 11)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.save()
    S = Settlement.objects.get(id = 12)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.save()
    S = Settlement.objects.get(id = 12)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 13)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.save()
    S = Settlement.objects.get(id = 13)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 13)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 14)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 14)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 14)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 15)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 15)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.save()
    S = Settlement.objects.get(id = 15)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 16)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 16)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.save()
    S = Settlement.objects.get(id = 16)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 17)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.save()
    S = Settlement.objects.get(id = 17)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 17)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 18)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 18)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 19)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 21)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.save()
    S = Settlement.objects.get(id = 22)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.save()
    S = Settlement.objects.get(id = 22)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 23)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.save()
    S = Settlement.objects.get(id = 23)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 23)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 24)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 24)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 24)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 25)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 25)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 25)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.save()
    S = Settlement.objects.get(id = 26)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.save()
    S = Settlement.objects.get(id = 26)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 26)
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 27)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.save()
    S = Settlement.objects.get(id = 27)
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 27)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 28)
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 28)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 28)
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 29)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 29)
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 30)
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 31)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 32)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 32)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 33)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 33)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 33)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 34)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 34)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 34)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 35)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 35)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 35)
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 36)
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 36)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 36)
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 37)
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 37)
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 37)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.save()
    S = Settlement.objects.get(id = 38)
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 38)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.save()
    S = Settlement.objects.get(id = 38)
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 39)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.save()
    S = Settlement.objects.get(id = 39)
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 40)
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 41)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 42)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 42)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 43)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 43)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 43)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 44)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 44)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 44)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.save()
    S = Settlement.objects.get(id = 45)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 45)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.save()
    S = Settlement.objects.get(id = 45)
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 46)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.save()
    S = Settlement.objects.get(id = 46)
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 46)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 47)
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 47)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 47)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.save()
    S = Settlement.objects.get(id = 48)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 48)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.save()
    S = Settlement.objects.get(id = 49)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.save()
    S = Settlement.objects.get(id = 50)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 51)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 52)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 52)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.save()
    S = Settlement.objects.get(id = 53)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.save()
    S = Settlement.objects.get(id = 54)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.save()
    S = Settlement.objects.get(id = 54)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 55)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 56)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    return redirect('/game')