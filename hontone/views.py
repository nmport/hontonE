from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from hontone.forms import NameForm
from hontone.models import HontoneUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

MAX_USERNAME_LENGTH = 15

def login(request):
    if request.method == 'POST':
        # we go here if the method is a POST
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            is_new_user = form.cleaned_data['is_new_user']
            print(is_new_user)
            if is_new_user:
                # this means the user selected new user and wants to register 
                if HontoneUser.objects.filter(username=username).exists():
                    # we are checking if the username they picked exists and returning an error message and reloading the page
                    return render(request, 'login.html', {'error_msg': 'Username already exists','form': form})
                if len(username) not in range(2, MAX_USERNAME_LENGTH+1):
                    return render(request, 'login.html', {'error_msg': f'Usernames must between 2 and {MAX_USERNAME_LENGTH} characters','form': form})
                user = HontoneUser.objects.create_user(username=username, password=password)
            else:
                # otherwise, they are an existing user and should be logged in
                user = authenticate(username=username, password=password)
                if not user:
                    # the authenticate returns None if the user inputted an incorrect username or password, 
                    # so returning an error message here as well
                    return render(request, 'login.html', {'error_msg': 'Username/Password is not valid','form': form})
            # authenticate user and redirect them to the home page, more stuff to do with this later
            auth_login(request, user)
        return redirect('home')
    else:
        # if not a POST we go here (which will normally be a GET but who knows what the user will do)
        form = NameForm()
        return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required(login_url='/login')
def show_users(request):
    users = HontoneUser.objects.all()
    context = {
        'users': users
    }
    return render(request, 'users.html', context)
