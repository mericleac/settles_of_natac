from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
import json

def index(request):
    if 'log' not in request.session:
        request.session['log'] = []
    players = request.session['player']
    all_players = []
    for each in players:
        p = Player.objects.get(id=each)
        all_players.append(p)
    return render(request, "main_game/index.html", { 'player': Player.objects.get(id=request.session['currPlayer']), 'log': request.session['log'], 'all_players':all_players })
    
def roll_dice(request):
    log = []
    #print(log)
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
    request.session['dice'] = 'rolled'
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
        "dice": request.session['dice']
    }
    return JsonResponse(json.dumps(context), safe = False)


def setup(request):
    print("Here?")
    request.session['currPlayer'] = request.session['player'][0]
    request.session['setup'] = True
    request.session['setup_round'] = 1
    request.session['sett_or_road'] = "settlement"
    return redirect('/game')

def player_turn(request):
    for i in range(len(request.session['player'])):
        if request.session['player'][i] == request.session['currPlayer']:
            break
    player = Player.objects.get(id=request.session['currPlayer'])
    if player.vic_points >= 10:
        return redirect("/game/victory/" + str(request.session['currPlayer']))
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
    request.session['dice'] = 'unrolled'
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
        "dice": request.session['dice']
    }
    print("The current player is now "+ context['player_info']['name'])
    print("currPlayer is:", curr_player.name)
    return JsonResponse(json.dumps(context), safe = False)

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
    if settlement.player == player and settlement.rank == "normal":
        city = True
        player.vic_points += 1
        player.save()
        errors = settlement.purchase_settlement(player, True)
    elif settlement.player != player:
        city = False
        errors = settlement.purchase_settlement(player, False)
    else:
        errors = ["You can only upgrade a settlement once!"]
    if len(errors) == 0:
        if city == False:
            player.brick -= 1
            player.lumber -= 1
            player.sheep -= 1
            player.wheat -= 1
            player.vic_points += 1
            player.save()
            settlement.player = player
            settlement.save()
        else: 
            player.ore -= 3
            player.wheat -= 2
            player.save()
            settlement.rank = "city"
            settlement.save()
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
            "city": city,
            "settlements": settle_dict,
            "roads": road_dict,
            "success": True,
            "setup": request.session['setup'],
        }
        return JsonResponse(json.dumps(context), safe = False)
    else:
        request.session['errors'] = errors
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        settlement = Settlement.objects.get(id= int(settlement_id))
        roads = Road.objects.all()
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
            "errors": errors,
            "settlements": settle_dict,
            "roads": road_dict,
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
            return JsonResponse(json.dumps(context), safe=False)
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
            "settlements": settle_dict,
            "roads": road_dict,
            "success": True,
            "setup": request.session['setup'],
        }
        return JsonResponse(json.dumps(context), safe = False)
    else:
        request.session['errors'] = errors
        print(*errors)
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
            "settlements": settle_dict,
            "roads": road_dict,
            'errors': errors,
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
    return redirect("/lobby")

def victory (request, player_id):
    player = Player.objects.get(id = int(player_id))
    return render(request, "main_game/victory.html", { "Victor": player })

def initialize_db(request):
    for field in Field.objects.all():
        field.delete()
    for road in Road.objects.all():
        road.delete()
    for settlement in Settlement.objects.all():
        settlement.delete()
    arr=['ore','ore','ore','brick','brick','brick','wheat','wheat','wheat','wheat','sheep','sheep','sheep','sheep','lumber','lumber','lumber','lumber', 'none']
    num_arr=[11, 12, 9, 4, 6, 5, 10, 3, 11, 4, 8, 8, 10, 9, 3, 5, 2, 6, 7]
    field_dict={}
    num_dict={}
    for num in range(1, 20):
        import random
        rand = random.randint(0, len(arr) - 1)
        field_dict[num] = arr[rand]
        num_dict[num] = num_arr[rand]
        num_arr.remove(num_arr[rand])
        arr.remove(arr[rand])
    print(field_dict)
    for num in range(1, 20):
        Field.objects.create(
            id = num,
            resource = field_dict[num],
            robber = False,
            number = num_dict[num]
        )

    for i in range (1, 73):
        road = Road(id=i)
        road.save()
    for i in range (1, 55):
        settlement = Settlement(id=i)
        settlement.save()
    for i in range (1, 7):
        print(i)
        R = Road.objects.get(id=i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i+1)))
        R.save()
    for i in range (11, 19):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = i-3))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-2)))
        R.save()
    for i in range(24, 34):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-7)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-6)))
        R.save()
    for i in range(40, 50):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 12)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 11)))
        R.save()
    for i in range(55, 63):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 16)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 15)))
        R.save()
    for i in range(67, 73):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-19)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i-18)))
        R.save()
    count = 0
    for i in range(7, 11):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 6 + count)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i + 2 + count)))
        R.save()
        count += 1
    count = 0
    for i in range(19, 24):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 11 + count)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 1 + count)))
        R.save()
        count += 1
    count = 0
    for i in range(34, 40):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 17 + count)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 6 + count)))
        R.save()
        count += 1
    count = 0
    for i in range(50, 55):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 21 + count)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 11 + count)))
        R.save()
        count += 1
    count = 0
    for i in range(63, 67):
        R = Road.objects.get(id = i)
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 23 + count)))
        R.adjacent_settlements.add(Settlement.objects.get(id = (i - 15 + count)))
        R.save()
        count += 1
    S = Settlement.objects.get(id = 1)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 2)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 3)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 4)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 5)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 6)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 7)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 8)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.save()
    S = Settlement.objects.get(id = 9)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.save()
    S = Settlement.objects.get(id = 10)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.save()
    S = Settlement.objects.get(id = 11)
    S.adjacent_fields.add(Field.objects.get(id = 1))
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 12)
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.save()
    S = Settlement.objects.get(id = 13)
    S.adjacent_fields.add(Field.objects.get(id = 2))
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.save()
    S = Settlement.objects.get(id = 14)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 15)
    S.adjacent_fields.add(Field.objects.get(id = 3))
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 16)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 17)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 18)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 19)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 20)
    S.adjacent_fields.add(Field.objects.get(id = 4))
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 21)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 22)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.adjacent_fields.add(Field.objects.get(id = 5))
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.save()
    S = Settlement.objects.get(id = 23)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 24)
    S.adjacent_fields.add(Field.objects.get(id = 6))
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 25)
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 26)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.adjacent_fields.add(Field.objects.get(id = 7))
    S.save()
    S = Settlement.objects.get(id = 27)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 28)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.save()
    S = Settlement.objects.get(id = 29)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 30)
    S.adjacent_fields.add(Field.objects.get(id = 8))
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.save()
    S = Settlement.objects.get(id = 31)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 32)
    S.adjacent_fields.add(Field.objects.get(id = 9))
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 33)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 34)
    S.adjacent_fields.add(Field.objects.get(id = 10))
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.save()
    S = Settlement.objects.get(id = 35)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 36)
    S.adjacent_fields.add(Field.objects.get(id = 11))
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 37)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 38)
    S.adjacent_fields.add(Field.objects.get(id = 12))
    S.save()
    S = Settlement.objects.get(id = 39)
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 40)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.save()
    S = Settlement.objects.get(id = 41)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.adjacent_fields.add(Field.objects.get(id = 13))
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.save()
    S = Settlement.objects.get(id = 42)
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 43)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.adjacent_fields.add(Field.objects.get(id = 14))
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.save()
    S = Settlement.objects.get(id = 44)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.adjacent_fields.add(Field.objects.get(id = 19))
    S.save()
    S = Settlement.objects.get(id = 45)
    S.adjacent_fields.add(Field.objects.get(id = 15))
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.adjacent_fields.add(Field.objects.get(id = 19))
    S.save()
    S = Settlement.objects.get(id = 46)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.adjacent_fields.add(Field.objects.get(id = 19))
    S.save()
    S = Settlement.objects.get(id = 47)
    S.adjacent_fields.add(Field.objects.get(id = 16))
    S.save()
    S = Settlement.objects.get(id = 48)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.save()
    S = Settlement.objects.get(id = 49)
    S.adjacent_fields.add(Field.objects.get(id = 17))
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 51)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.save()
    S = Settlement.objects.get(id = 52)
    S.adjacent_fields.add(Field.objects.get(id = 18))
    S.adjacent_fields.add(Field.objects.get(id = 19))
    S.save()
    S = Settlement.objects.get(id = 53)
    S.adjacent_fields.add(Field.objects.get(id = 19))
    S.save()
    S = Settlement.objects.get(id = 54)
    S.adjacent_fields.add(Field.objects.get(id = 19))
    S.save()

    fields = {}
    num_dict = {}

    for field in Field.objects.all():
        fields[field.id] = field.resource
        num_dict[field.id] = field.number

    player = Player.objects.get(id = request.session['currPlayer'])
    context = {
        'field_dict': {
            'wheat': 'field',
            'brick': 'hill',
            'ore': 'mountain',
            'lumber': 'forest',
            'sheep': 'pasture',
            'none': 'desert'
        },
        'fields': fields,
        'num_dict': num_dict,
        'player': player.name,
    }
    return JsonResponse(json.dumps(context), safe=False)