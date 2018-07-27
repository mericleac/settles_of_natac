from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request, id):
    
    playerA = Player.objects.get(id = request.session['currPlayer'])
    playerB = Player.objects.get(id = id)
    request.session['tradePartner'] = playerB.id
    if playerA == playerB:
        print("You can not trade with yourself!")
        return redirect('/game')
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
    print("*"*80)
    print(playerA.name, "vp:", playerA.vic_points, "wheat:", playerA.wheat, "ore:", playerA.ore, "brick", playerA.brick, "lumber:", playerA.lumber, "sheep:", playerA.sheep, )
    print(playerB.name, "vp:", playerB.vic_points, "wheat:", playerB.wheat, "ore:", playerB.ore, "brick", playerB.brick, "lumber:", playerB.lumber, "sheep:", playerB.sheep, )
    return redirect("/game")

def bank(request):
    playerA = Player.objects.get(id = request.session['currPlayer'])
    request.session['tradePartner'] = "bank"
    context = {
        'p1': playerA,
        'p2': "Bank"
    }
    return render(request, "trading/tradeBank.html", context)

def trade_bank(request):
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
        messages.error(request, "Resources given away not multiple of 4", "tradeError")
        return redirect('/trading/bank')
    elif (brick + sheep + ore + wheat + lumber) == (int(request.POST['p2brick'])*4 + int(request.POST['p2sheep'])*4 + int(request.POST['p2ore'])*4 + int(request.POST['p2wheat'])*4 + int(request.POST['p2lumber'])*4):
        playerA = Player.objects.get(id=request.session['currPlayer'])
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
        return redirect('/trading/bank')
    return redirect('/game')

def delete(request):
    Player.objects.all().delete()
    return HttpResponse("deleted")