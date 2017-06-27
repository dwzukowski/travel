# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt 
NAME_REGEX = re.compile(r'^[a-zA-Z ]+ [a-zA-Z0-9_]{3,}$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]{3,}$')

class UsersManager(models.Manager):
    def add(self, name, userName, password, confirmpassword):
        messages= []
        checkusername= User.usersManager.filter(userName=userName)
        if len(checkusername) > 0:
            messages.append('This user name is already in database, please log in')
            return (False, messages)
        if not NAME_REGEX.match(name):
            messages.append('Name is a required field and can only contain letters')
        if not USERNAME_REGEX.match(userName):
            messages.append('Not a valid username')
        if len(name) < 1:
            messages.append('Name is required')
        elif len(name) < 3:
            messages.append('Name must be at least three characters') 
        if len(userName) < 1:
            messages.append('Username is required')
        elif len(userName) < 3:
            messages.append('Username must be at least three characters')            
        if password != confirmpassword:
            messages.append('Password does not match password confirmation')
        if len(messages) == 0:
            hashedPassword= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
            user= User.usersManager.create(name=name, userName=userName, password=hashedPassword)
            return (True, user)
        return (False, messages)
    def loginValidation(self, userName, password):
        messages= []
        user = User.usersManager.filter(userName=userName)
        if len(user) < 1:
            messages.append('Username not found')
            return (False, messages)
        if bcrypt.hashpw(password.encode('utf-8'), user[0].password.encode('utf-8')) != user[0].password.encode('utf-8'):
            messages.append('Incorrect password')
            return (False, messages)
        else:
            user= user[0].id
            return (True, user)
class TripsManager(models.Manager):
    def add(self, destination, description, start, end, user):
        messages= []
        if len(destination) < 1:
            messages.append('Destination is required')
        if len(description) < 1:
            messages.append('Description is required')
        if len(start) < 1 or len(end) < 1:
            messages.append('Trip start and end dates are required')               
        if len(messages) == 0:
            trip= Trip.tripsManager.create(destination=destination, description=description, start=start, end=end, user_id=user)
            return (True, 'trip')
        return (False, messages)
class TripfriendsManager(models.Manager):
    def add(self, trip, user):
        messages=[]
        check= Tripfriend.tripfriendsManager.filter(trip_id=trip, friend_id=user)
        if len(check) > 0:
            messages.append('You already joined this trip')
            return (False, messages)      
        else:
            tripfriend= Tripfriend.tripfriendsManager.create(trip_id=trip, friend_id=user)
            return (True, tripfriend)
class User(models.Model):
    name= models.CharField(max_length=255)
    userName= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    usersManager= UsersManager()
class Trip(models.Model):
    destination= models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    start= models.DateField()
    end= models.DateField()
    user= models.ForeignKey(User)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    tripsManager= TripsManager()
class Tripfriend(models.Model):
    trip= models.ForeignKey(Trip)
    friend= models.ForeignKey(User)
    tripfriendsManager= TripfriendsManager()