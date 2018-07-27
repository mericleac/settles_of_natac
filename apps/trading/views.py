from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django.contrib import messages
import json

def index(request, id):
    
    playerA = Player.objects.get(id = request.session['currPlayer'])
    playerB = Player.objects.get(id = id)
    request.session['tradePartner'] = playerB.id
    if playerA == playerB:
        context = {
            "error": "You cannot trade with yourself!"
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

def bank(request):
    playerA = Player.objects.get(id = request.session['currPlayer'])
    request.session['tradePartner'] = "bank"
    context = {
        'p1': playerA,
        'p2': "Bank"
    }
    return render(request, "trading/tradeBank.html", context)

def trade_bank(request):
    playerA = Player.objects.get(id=request.session['currPlayer'])
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
    print("*"*80)
    print(request.POST['p1brick'])
    print(request.POST['p1sheep'])
    print(request.POST['p1ore'])
    print(request.POST['p1wheat'])
    print(request.POST['p1lumber'])
    brick = int(request.POST['p1brick'])
    sheep = int(request.POST['p1sheep'])
    ore = int(request.POST['p1ore'])
    wheat = int(request.POST['p1wheat'])
    lumber = int(request.POST['p1lumber'])

    print(type(ore))
    if brick % 4 != 0 or sheep % 4 != 0 or ore % 4 != 0 or wheat % 4 != 0 or lumber % 4 != 0:
        print("Not multiple of 4!")
        print("have i broke yet")
        context = {
            "Error": "Resources given away not multiple of 4!"
        }
        return JsonResponse(json.dumps(context), safe = False)
    elif (brick + sheep + ore + wheat + lumber) == (int(request.POST['p2brick'])*4 + int(request.POST['p2sheep'])*4 + int(request.POST['p2ore'])*4 + int(request.POST['p2wheat'])*4 + int(request.POST['p2lumber'])*4):
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
        playerA.save()
    else:
        print("not equal")
        messages.error(request, "Resources given/taken do not match quantities", "tradeError")
        return JsonResponse(json.dumps(context), safe = False)
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

def delete(request):
    Player.objects.all().delete()
    return HttpResponse("deleted")