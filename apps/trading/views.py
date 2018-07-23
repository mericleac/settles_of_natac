from django.shortcuts import render, HttpResponse, redirect
from .models import *

def create(request):
    playerA = Player.objects.create(name="Alice", vic_points=0, wheat=5, ore=5, brick=5, lumber=5, sheep=5)
    playerB = Player.objects.create(name="Bob", vic_points=0, wheat=3, ore=3, brick=3, lumber=3, sheep=3)
    return redirect("/trading")

def index(request):
    playerA = Player.objects.get(name="Alice")
    playerB = Player.objects.get(name="Bob")
    context = {
        'p1': playerA,
        'p2': playerB,
        'jinjasux': [0, 1, 2, 3, 4]
    }
    print("*"*100)
    print(context['p2'].sheep)
    return render(request, "trading/trade.html")

def trade(request):
    playerA = Player.objects.get(name="Alice")
    playerB = Player.objects.get(name="Bob")
    print("*"*120)
    print(request.POST)
    print(playerA.wheat)
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