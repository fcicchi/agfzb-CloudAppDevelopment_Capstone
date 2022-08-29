from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def login_request(request):
    context = {} 
    if request.method == "POST":
        user = request.POST['user']
        password = request.POST['password']
        user = authenticate(username=user, password=password)

        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            resp =  redirect('djangoapp:index')
            resp['Location'] += '?msg=login_failed'
            return resp
    else:
        return redirect('djangoapp:index')

def logout_request(request):
    resp =  redirect('djangoapp:index')
    resp['Location'] += '?msg=logout&user=' + request.user.username
    logout(request)
    return resp

def registration_request(request):
    context = {}
    return render(request, 'djangoapp/registration.html', context)

def signup_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['password']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_exist = False

        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))

        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect('djangoapp:index')

        else:
            resp =  redirect('djangoapp:register')
            resp['Location'] += '?signin=exist'
            logout(request)
            return resp

    else:
        return redirect('djangoapp:register')



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...