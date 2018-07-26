from django.db import models
import re

class PlayerManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['player1Name']) == 1:
            errors['player1Name'] = "Name must be longer than 1 character!"
        if len(post_data['player2Name']) == 1:
            errors['player2Name'] = "Name must be longer than 1 character!"
        if len(post_data['player3Name']) == 1:
            errors['player3Name'] = "Name must be longer than 1 character!"
        if len(post_data['player4Name']) == 1:
            errors['player4Name'] = "Name must be longer than 1 character!"
        return errors

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['userName']) < 1:
            errors["userName"] = "Please enter a name!"
        if len(User.objects.filter(user_name=postData['userName'])) > 0:
            errors["userName"] = "User Name already taken. Please choose a different name."
        if not re.match(r"[^@]+@[^@]+\.[^@]+.", postData['email']):
            errors["email"] = "Invalid email."
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors["email"] = "This email is already registered."
        if len(postData['password']) < 8:
            errors["password"] = "Password must be longer than 8 characters."
        if len(postData['password']) >= 8:
            if postData['password'] != postData['passwordConf']:
                errors["passwordConf"] = "Passwords do not match."
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
    turn_index = models.IntegerField(null=True)
 
class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    password_confirmation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()