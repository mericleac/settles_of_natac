from django.db import models
from apps.login_reg_lobby.models import *

class Field(models.Model):
    resource = models.CharField(max_length = 45)
    #documentation on symmetrical many to many relationships- I don't think we've covered this in the platform yet,
    #o feel free to switch this line around if it looks like I've gotten the syntax off
    #https://docs.djangoproject.com/en/dev/ref/models/fields/#manytomanyfield 
    adjacent_fields = models.ManyToManyField("self")
    #I don't think the robber is in our MVP, but I'll leave this line here for now. We can do stuff with it later if we have time
    robber = models.BooleanField()

class Vertex(models.Model):
    adjacent_fields = models.ManyToManyField(Field, related_name = "adjacent_vertices")

class Edge(models.Model):
    adjacent_fields = models.ManyToManyField(Field, related_name = "adjacent_edges")
    adjacent_vertices = models.ManyToManyField(Vertex, related_name = "adjacent_edges")

class Settlement(models.Model):
    player = models.ForeignKey(Player, related_name = "settlements")
    vertex = models.OneToOneField(Vertex)

class City(models.Model):
    player = models.ForeignKey(Player, related_name = "cities")
    vertex = models.OneToOneField(Vertex)

class Road(models.Model):
    player = models.ForeignKey(Player, related_name = "roads")
    edge = models.OneToOneField(Edge)

class DevCard(models.Model):
    player = models.ForeignKey(Player, related_name = "devcards")
    name = models.CharField(max_length = 45)