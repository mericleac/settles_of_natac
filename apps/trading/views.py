from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
import json

def index(request, id):
    print("Made it here")
    playerA = Player.objects.get(id = request.session['currPlayer'])
    playerB = Player.objects.get(id = id)
    request.session['tradePartner'] = playerB.id
    if playerA == playerB:
        roads = Road.objects.all()
        settlements = Settlement.objects.all()
        settle_dict = {}
        for settlement in settlements:
            settle_dict[settlement.id] = settlement.is_owned()
        road_dict = {}
        for road in roads:
            road_dict[road.id] = road.is_owned()
        context = {
            "Error": "You cannot trade with yourself!"
        }
        return JsonResponse(json.dumps(context), safe = False)
    context = {
        'p1': playerA,
        'p2': playerB
    }
    return render(request, "trading/trade.html", context)

def trade(request):
    playerA = Player.objects.get(id=request.session['currPlayer'])
    playerB = Player.objects.get(id=request.session['tradePartner'])
    playerA.wheat += int(request.POST['p2wheat'])
    playerA.ore += int(request.POST['p2ore'])
    playerA.brick += int(request.POST['p2brick'])
    playerA.lumber += int(request.POST['p2lumber'])
    playerA.sheep += int(request.POST['p2sheep'])
    playerA.wheat -= int(request.POST['p1wheat'])
    playerA.ore -= int(request.POST['p1ore'])
    playerA.brick -= int(request.POST['p1brick'])
    playerA.lumber -= int(request.POST['p1lumber'])
    playerA.sheep -= int(request.POST['p1sheep'])
    playerB.wheat += int(request.POST['p1wheat'])
    playerB.ore += int(request.POST['p1ore'])
    playerB.brick += int(request.POST['p1brick'])
    playerB.lumber += int(request.POST['p1lumber'])
    playerB.sheep += int(request.POST['p1sheep'])
    playerB.wheat -= int(request.POST['p2wheat'])
    playerB.ore -= int(request.POST['p2ore'])
    playerB.brick -= int(request.POST['p2brick'])
    playerB.lumber -= int(request.POST['p2lumber'])
    playerB.sheep -= int(request.POST['p2sheep'])
    playerA.save()
    playerB.save()
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
            "name": playerA.name,
            "brick": playerA.brick,
            "sheep": playerA.sheep,
            "ore": playerA.ore,
            "wheat": playerA.wheat,
            "lumber": playerA.lumber,
            "vic_points": playerA.vic_points,
        },
        "settlements": settle_dict,
        "roads": road_dict,
        "same_player": "no"
    }
    return JsonResponse(json.dumps(context), safe = False)

def nvm(request):
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
        "settlements": settle_dict,
        "roads": road_dict,
    }
    return render(request, "main_game/index.html", context)

def delete(request):
    Player.objects.all().delete()
    return HttpResponse("deleted")