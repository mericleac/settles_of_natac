from django.shortcuts import render, redirect, HttpResponse
from .models import *

def setup_settlementr1(request, settlement_id):
    print("Setting up settlement")
    settlement = Settlement.objects.get(id=settlement_id)
    player = Player.objects.get(id=request.session['currPlayer'])
    settlement.player = player
    settlement.save()
    print(request.session['sett_or_road'])
    request.session['sett_or_road'] = "road"
    print(request.session['sett_or_road'])
    return render(request, "main_game/info.html", { 'player': Player.objects.get(id=request.session['currPlayer'])})

def setup_roadr1(request, road_id):
    print("Setting up road")
    road = Road.objects.get(id=road_id)
    player = Player.objects.get(id=request.session['currPlayer'])
    road.player = player
    road.save()
    request.session['sett_or_road'] = "settlement"
    return redirect('/setup/end_turn')

def end_turn(request):
    print("In Setup's end turn")
    players = request.session['player']
    print(players)
    player = request.session['currPlayer']
    if request.session['setup_round'] == 1:
        if player == players[-1]:
            request.session['setup_round'] = 2
            return render(request, "main_game/info.html", { 'player': Player.objects.get(id=request.session['currPlayer'])})
        request.session['currPlayer'] = player+1
        print(request.session['currPlayer'])
    elif request.session['setup_round'] == 2:
        if request.session['currPlayer'] != players[0]:
            request.session['currPlayer'] = player-1
        else:
            request.session['setup'] = False
            print("Ending setup")
            return render(request, "main_game/info.html", { 'player': Player.objects.get(id=request.session['currPlayer'])})
    print(request.session['currPlayer'])
    return render(request, "main_game/info.html", { 'player': Player.objects.get(id=request.session['currPlayer'])})