# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
#from .models import User, Book, Review, Author
from django.contrib import messages
from .models import User, Trip, Tripfriend
from datetime import datetime 
import bcrypt 

def index(request):
    return render(request, 'firstapp/index.html')
def register(request):
    check= User.usersManager.add(request.POST['name'], request.POST['userName'], request.POST['password'], request.POST['confirmpassword'])
    if not check[0]:
        for message in check[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
    else:
        request.session['loggedinUser']= check[1].id
        return redirect('/travels')
def travels(request):
    if not 'loggedinUser' in request.session:
        messages.add_message(request, messages.ERROR, 'Please sign in')
        return redirect('/')
    else:
        context={
            'users': User.usersManager.all(),
            'trips': Trip.tripsManager.all().order_by('-created_at'),
        }
        return render(request, 'firstapp/travels.html',context)
def logout(request):
    request.session.clear()
    return redirect('/')
def login(request):
    check= User.usersManager.loginValidation(request.POST['userName'], request.POST['password'])
    if not check[0]:
        for message in check[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
    else:
        request.session['loggedinUser']= check[1]
        return redirect('/travels')
def addtravel(request):
    return render(request, 'firstapp/addtravel.html')
def addtrip(request):
    start= request.POST['start']
    end= request.POST['end']
    now= datetime.now()
    if start > end:
        messages.add_message(request, messages.ERROR, 'A trip cannot end before it starts')
        return redirect('/addtravel')
    clean_start= datetime.strptime(start, '%Y-%m-%d')
    if clean_start < now:
        messages.add_message(request, messages.ERROR, 'Time travel not yet viable. A trip can\'t begin in the past')
        return redirect('/addtravel')
    check= Trip.tripsManager.add(request.POST['destination'], request.POST['description'], str(request.POST['start']), str(request.POST['end']), request.session['loggedinUser']) 
    if not check[0]:
        for message in check[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/addtravel')
    else:
        return redirect('/travels')
    return redirect('/addtravel')
def showtrip(request, trip_id):
    context={
        'trips': Trip.tripsManager.get(id=trip_id),
        'tripfriends': Tripfriend.tripfriendsManager.filter(trip_id=trip_id)
    }
    return render(request, 'firstapp/destination.html', context)
def jointrip(request, trip_id):
    trip= Trip.tripsManager.get(id=trip_id)
    if trip.user.id == request.session['loggedinUser']:
        messages.add_message(request, messages.ERROR, "You can\'t join your own trip")
        return redirect('/travels')
    check= Tripfriend.tripfriendsManager.add(trip_id, request.session['loggedinUser'])
    if not check[0]:
        for message in check[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/travels')
    else:
        messages.add_message(request, messages.SUCCESS, "You joined a trip!")
        return redirect('/travels')