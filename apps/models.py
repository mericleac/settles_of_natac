from django.db import models
import re

class PlayerManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['name']) == 0:
            errors['name'] = You must enter a name!
        return errors

class Player(models.Model):
    name = models.CharField(max_length = 45)
    vic_points = models.IntegerField()
    wheat = models.IntegerField()
    ore = models.IntegerField()
    brick = models.IntegerField()
    lumber = models.IntegerField()
    sheep = models.IntegerField()
    objects = PlayerManager()

class Field(models.Model):
    resource = models.CharField(max_length = 45)
    #documentation on symmetrical many to many relationships- I don't think we've covered this in the platform yet,
    #o feel free to switch this line around if it looks like I've gotten the syntax off
    #https://docs.djangoproject.com/en/dev/ref/models/fields/#manytomanyfield 
    adjacent_fields = models.ManyToManyField(self)
    #I don't think the robber is in our MVP, but I'll leave this line here for now. We can do stuff with it later if we have timme
    robber = models.BooleanField()

# I don't think we need this, we can just set up a direct relationship between fields and settlements
# class Vertex(models.Model):
#     adjacent_fields = models.ManyToManyField(Field, related_name = "adjacent_vertices")

# This can also be a direct relationship between 
# class Edge(models.Model):
#     adjacent_fields = models.ManyToManyField(Field, related_name = "adjacent_edges")
#     adjacent_vertices = models.ManyToManyField(FieldVertex, related_name = "adjacent_edges")

class Settlement(models.Model):
    player = models.ForeignKey(Player, related_name = "settlements")
    # added rank field in order to consolidate settlements and cities
    rank = models.CharField(max_length = 45, default="normal")
    # changed this relationship to be with fields instead
    adjacent_fields = models.ManyToManyField(Field, related_name="adjacent_settlements")

# Cities and settlements can be grouped together if we add a rank field to settlements and set it to "city" if a
# city is built or a settlement is upgraded
# class City(models.Model):
#     player = models.ForeignKey(Player, related_name = "cities")
#     vertex = models.OneToOneField(Vertex)

class Road(models.Model):
    player = models.ForeignKey(Player, related_name = "roads")
    # changed this relationship to be with fields instead
    adjacent_fields = models.ManyToManyField(Field, related_name="adjacent_roads")

class DevCard(models.Model):
    player = models.ForeignKey(Player, related_name = "devcards")
    name = models.CharField(max_length = 45)