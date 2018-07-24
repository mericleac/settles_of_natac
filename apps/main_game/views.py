from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    return render(request, "main_game/index.html")

def roll_dice(request):
    from random import randint
    die1 = randint(1, 6)
    print('first dice was: ', die1)
    die2 = randint(1, 6)
    print('second dice was: ', die2)
    print('total was: ', die1 + die2)
    rolled = Field.objects.filter(number=die1 + die2)
    if len(rolled) == 0:
        print('no field matched the roll')
    else:
        for field in rolled:
            print('alloting resources for: ', field.number, field.resource)
            field.distribute_resources()
    player1 = Player.objects.last()
    print(player1.name, "has:")
    print("Lumber: ", player1.lumber)
    print("Sheep: ", player1.sheep)
    print("Wheat: ", player1.wheat)
    print("Brick: ", player1.brick)
    print("Ore: ", player1.ore)
    return redirect('/game')