from django.db import models
from apps.login_reg_lobby.models import *

class Field(models.Model):
    resource = models.CharField(max_length = 45)
    #documentation on symmetrical many to many relationships- I don't think we've covered this in the platform yet,
    #o feel free to switch this line around if it looks like I've gotten the syntax off
    #https://docs.djangoproject.com/en/dev/ref/models/fields/#manytomanyfield 
    adjacent_fields = models.ManyToManyField("self")
    # added number to check dice rolls against
    number = models.IntegerField()
    #I don't think the robber is in our MVP, but I'll leave this line here for now. We can do stuff with it later if we have time
    robber = models.BooleanField()
    def distribute_resources (self):
        log = []
        for settlement in self.adjacent_settlements.all():
            if settlement.player != None:
                player = settlement.player
                if settlement.rank == "city":
                    log.append("Alloting resources to " + player.name + "'s city.")
                    player.__dict__[self.resource] += 2
                    player.save()
                else: 
                    log.append("Alloting resources to " + player.name + "'s settlement.")
                    player.__dict__[str(self.resource)] += 1
                    player.save()
        return log

class Settlement(models.Model):
    def is_owned(self):
        if self.player == None:
            return False
        else:
            return self.player.turn_index
    def purchase_settlement(self, player, city):
        errors = []
        if self.player != None:
            if self.player == player:
                city = True
            else:
                errors.append("That settlement is already owned!")
        if city == False:
            if player.brick < 1 or player.lumber < 1 or player.sheep < 1 or player.wheat < 1:
                errors.append("Not enough resources!")
        else:
            if player.ore < 3 or player.wheat < 2:
                errors.append("Not enough resources!")
        owned_road = False
        spaced_out = True
        for road in self.adjacent_roads.all():
            if road.player == player:
                owned_road = True
            for settlement in road.adjacent_settlements.all():
                if settlement.player != None and settlement != self:
                    spaced_out = False
        if owned_road == False:
            errors.append("You must own a road adjoining a settlement in order to purchase it!")
        if spaced_out == False:
            errors.append("You may only build a settlement if the intersection adjacent to it are vacant!")
        return errors

    def setup_settlement(self, player, city):
        errors = []
        if self.player != None:
            errors.append("That settlement is already owned!")
        spaced_out = True
        for road in self.adjacent_roads.all():
            for settlement in road.adjacent_settlements.all():
                if settlement.player != None:
                    spaced_out = False
        if spaced_out == False:
            errors.append("You may only build a settlement if the intersections adjacent to it are vacant!")
        return errors

    player = models.ForeignKey(Player, related_name = "settlements", default=None, null=True)
    rank = models.CharField(max_length = 45, default="normal")
    adjacent_fields = models.ManyToManyField(Field, related_name="adjacent_settlements")

class Road(models.Model):
    def is_owned(self):
        if self.player == None:
            return False
        else:
            return self.player.turn_index
            
    def setup_road (self, player, city):
        errors = []
        owned_settlement = False
        for settlement in self.adjacent_settlements.all():
            print(player.settlements.all().values())
            if settlement.player == player:
                owned_settlement = True
            else:
                for adjacent_road in settlement.adjacent_roads.all():
                    if adjacent_road.player == player:
                        owned_settlement = True
        if self.player != None:
            errors.append("That road is already owned!")
        if owned_settlement == False:
            errors.append("Your road must be connected to a settlement or road that you own!")
        print(errors)
        return errors
    def purchase_road (self, player):
        errors = []
        owned_settlement = False
        owned_road = False
        for settlement in self.adjacent_settlements.all():
            if settlement.player == player:
                owned_settlement = True
            else:
                for adjacent_road in settlement.adjacent_roads.all():
                    if adjacent_road.player == player:
                        owned_settlement = True
        if self.player != None:
            errors.append("That road is already owned!")
        if player.brick < 1 or player.lumber < 1:
            errors.append("Not enough resources!")
        if owned_settlement == False:
            errors.append("Your road must be connected to a settlement or road that you own!")
        print(errors)
        return errors

    player = models.ForeignKey(Player, related_name = "roads", default = None, null=True)
    adjacent_settlements = models.ManyToManyField(Settlement, related_name="adjacent_roads")

class DevCard(models.Model):
    player = models.ForeignKey(Player, related_name = "devcards")
    name = models.CharField(max_length = 45)