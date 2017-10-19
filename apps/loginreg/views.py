# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'loginreg/index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors['error'])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password = hashed_pw)
        request.session['id'] = user.id
        return redirect('/success')

def login(request):
    login = User.objects.login(request.POST)
    errors = User.objects.login(request.POST)
    if 'user' in login:
        request.session['id'] = login['user'].id
        return redirect('/success')
    else:
        messages.error(request, login['error'])
        return redirect('/')

def success(request):
    context = {
        "users": User.objects.filter(id = request.session['id'])
    }
    return render(request, 'loginreg/success.html', context)

def logout(request):
    del request.session['id']
    return redirect('/')