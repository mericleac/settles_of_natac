from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import *
import json

def setup_settlementr1(request, settlement_id):
    print("Setting up settlement")
    settlement = Settlement.objects.get(id=settlement_id)
    player = Player.objects.get(id=request.session['currPlayer'])
    errors = settlement.setup_settlement(player, False)
    settlement.player = player
    settlement.save()
    print(request.session['sett_or_road'])
    request.session['sett_or_road'] = "road"
    print(request.session['sett_or_road'])
    context = {
        "player_info": {
            "name": player.name,
            "brick": player.brick,
            "sheep": player.sheep,
            "ore": player.ore,
            "wheat": player.wheat,
            "lumber": player.lumber,
            "vic_points": player.vic_points,
        }
    }
    return JsonResponse(json.dumps(context), safe = False)

def setup_roadr1(request, road_id):
    print("Setting up road")
    road = Road.objects.get(id=road_id)
    player = Player.objects.get(id=request.session['currPlayer'])
    errors = road.setup_road(player, False)
    road.player = player
    road.save()
    request.session['sett_or_road'] = "settlement"
    context = {
        "player_info": {
            "name": player.name,
            "brick": player.brick,
            "sheep": player.sheep,
            "ore": player.ore,
            "wheat": player.wheat,
            "lumber": player.lumber,
            "vic_points": player.vic_points,
        }
    }
    return redirect('/setup/end_turn')

def end_turn(request):
    print("In Setup's end turn")
    players = request.session['player']
    print(players)
    player = request.session['currPlayer']
    currPlayer = Player.objects.get(id=player)
    context = {
        "player_info": {
            "name": currPlayer.name,
            "brick": currPlayer.brick,
            "sheep": currPlayer.sheep,
            "ore": currPlayer.ore,
            "wheat": currPlayer.wheat,
            "lumber": currPlayer.lumber,
            "vic_points": currPlayer.vic_points,
        }
    }
    if request.session['setup_round'] == 1:
        if player == players[-1]:
            request.session['setup_round'] = 2
            return JsonResponse(json.dumps(context), safe = False)
        request.session['currPlayer'] = player+1
        print(request.session['currPlayer'])
    elif request.session['setup_round'] == 2:
        if request.session['currPlayer'] != players[0]:
            request.session['currPlayer'] = player-1
        else:
            request.session['setup'] = False
            print("Ending setup")
            return JsonResponse(json.dumps(context), safe = False)
    print(request.session['currPlayer'])
    return JsonResponse(json.dumps(context), safe = False)