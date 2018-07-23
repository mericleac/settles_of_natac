def rollDice(request):
    import random
    die1 = randint(1, 6)
    die2 = randint(1, 6)
    rolled = Terrain.objects.filter(number=die1 + die2)
    for terrain in rolled:
        terrain.distribute_resources
    return redirect('/game_map')

def distribute_resources (self):
    for settlement in self.adjacent_settlements:
        if settlement.player != None:
            player = settlement.player
            if settlement.rank == "city":
                player.__dict__[self.resource] += 2
            else: 
                player.__dict__[self.resource] += 1
    return self