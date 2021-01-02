from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
# Create your views here.

def home(request):
    return render(request, 'login.html')

def users(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user,
        'trips': Trip.objects.filter(trip_members=request.session['user_id']),
        'other_trips': Trip.objects.exclude(trip_members=request.session['user_id'])
    }
    return render(request, 'travels.html', context)

def register(request):
    if request.method == "GET":
        return redirect('/')
    # store id in req.session
    new_user = User.objects.register(request.POST['name'],  request.POST['username'],
                                     request.POST['password'], request.POST['passwordConfirm'])
    if new_user['status'] == True:
        request.session['id'] = new_user['created_user'].id
        return redirect('/users')
    else:
        messages.error(request, new_user['errors'], extra_tags="register")
        return redirect('/')


def login(request):
    if request.method == "GET":
        return redirect('/')
    current_user = User.objects.login_validate(request.POST['username'], request.POST['password'])
    if current_user['status'] == True:
        request.session['id'] = current_user['found_user'].id
        return redirect('/users')
    else:
        messages.error(request, current_user['errors'], extra_tags="login")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
