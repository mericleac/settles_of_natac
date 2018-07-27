from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):

    return render(request, 'login_html/index.html')

def register(request):

    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            request.session['userName'] = request.POST['userName']
            request.session['email'] = request.POST['email']
            for key, value in errors.items():
                print(key, value)
                messages.error(request, value, key)
            # This return statement means the user input generated errors. Redirect to same page
            return redirect('/register')
        else:
            newUser = User.objects.create(
                user_name = request.POST['userName'],
                email = request.POST['email'],
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()),
                password_confirmation = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                )
            messages.success(request, "Thanks for registering!", 'success')
            for key in request.session.keys():
                request.session[key] = ""
        # User input passed. New user created. Redirect to user home page 
        request.session['userId'] = newUser.id
        request.session['currUserName'] = newUser.user_name
        ###################################################################################
        #Need redirect route
        return redirect('/lobby')
    elif request.method == 'GET':
        return render(request, 'login_html/index.html')

def login(request):

    if request.method == 'POST':
        request.session['emailLogin'] = request.POST['email']
        if len(User.objects.filter(email=request.POST['email'])) < 1:
            messages.error(request, "Invalid login", "loginError")
            # Email didn't exist, redirect them to home page.
            return redirect('/login')
        confirm = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), confirm.password.encode()):
            print("Password matched!")
            request.session['userId'] = confirm.id
            request.session['currUserName'] = confirm.user_name
            # Sign in worked. Redirect to lobby. Track ID and Name.
            ###################################################################################
            #Need redirect route
            return redirect('/lobby')
        else:
            messages.error(request, "Invalid login", 'loginError')
            print("Password didn't match")
            # Wrong password. Reload page.
            return redirect('/login')
    if request.method == 'GET':
        return render(request, 'login_html/index.html')

def logout(request):
    for key in request.session.keys():
        request.session[key] = ""
    return redirect('/')

def lobby(request):
    return render(request, 'login_html/lobby.html')

def lobbyReg(request):
    errors = Player.objects.validator(request.POST)
    if len(errors):
        print("*"*80)
        print("there are errors")
        for key, value in errors.items():
            print(key, value)
            messages.error(request, value, key)
        # This return statement means the user input generated errors. Redirect to same page
        return redirect('/lobby')
    else:
        request.session['player'] = []
        if request.POST['player1Name']:
            p1 = Player.objects.create(
                name=request.POST['player1Name'], 
                vic_points=0, 
                wheat=0, 
                ore=0, 
                brick=0, 
                lumber=0, 
                sheep=0,
                turn_index=0
                )
            p1.save()
            request.session['player'].append(p1.id)
        if request.POST['player2Name']:
            p2 = Player.objects.create(
                name=request.POST['player2Name'], 
                vic_points=0, 
                wheat=0, 
                ore=0, 
                brick=0, 
                lumber=0, 
                sheep=0,
                turn_index=1,
                )
            p2.save()
            request.session['player'].append(p2.id)
        if request.POST['player3Name']:
            p3 = Player.objects.create(
                name=request.POST['player3Name'], 
                vic_points=0, 
                wheat=0, 
                ore=0, 
                brick=0, 
                lumber=0, 
                sheep=0,
                turn_index=2,
                )
            p3.save()
            request.session['player'].append(p3.id)
        if request.POST['player4Name']:
            p4 = Player.objects.create(
                name=request.POST['player4Name'], 
                vic_points=0, 
                wheat=0, 
                ore=0, 
                brick=0, 
                lumber=0, 
                sheep=0,
                turn_index=3,
                )
            p4.save()
            request.session['player'].append(p4.id)
        if len(request.session['player']) < 2:
            messages.error(request, 'Need to enter at least two players', 'playersCount')
            return redirect('/lobby')
        return redirect('/game/initialize_db')

