from django.shortcuts import render, HttpResponse, redirect
from .models import *

def create(request, id):
    playerA = Player.objects.get(id = request.session['currPlayer'])
    playerB = Player.objects.get(id = id)
    return redirect("/trading/"+id)

def index(request, id):
    playerA = Player.objects.get(id = request.session['currPlayer'])
    playerB = Player.objects.get(id = id)
    context = {
        'p1': playerA,
        'p2': playerB
    }
    return render(request, "trading/trade.html", context)

def trade(request):
    playerA = Player.objects.get(id=request.session['currPlayer'])
    playerB = Player.objects.last()
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
    return redirect("/trading")

def delete(request):
    Player.objects.all().delete()
    return HttpResponse("deleted")