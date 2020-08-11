from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here.

def home(request):
    return render(request, 'auth_module/home.html')


def signupuser(request):
    if request.user.is_authenticated:
        signupuserData = {'error':"You are already Logged in Kindly logout then signup"}
        return render(request, 'auth_module/errorpage.html', signupuserData)
    else:
        if request.method == 'GET':
            signupuserData = {'signupform':UserCreationForm}
            return render(request, 'auth_module/signupuser.html', signupuserData)
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except IntegrityError:
                    signupuserData = {'signupform':UserCreationForm, 'error':"Username Must be Unique"}
                    return render(request, 'auth_module/signupuser.html', signupuserData)                
            else:
                signupuserData = {'signupform':UserCreationForm, 'error':"Both Passwords must be same"}
                return render(request, 'auth_module/signupuser.html', signupuserData)


def loginuser(request):
    if request.method == 'GET':
        loginuserData = {'loginform':AuthenticationForm}
        return render(request, 'auth_module/loginuser.html', loginuserData)
    else:
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is None:
            loginuserData = {'loginform':AuthenticationForm, 'error':"Incorrect username or Password"}
            return render(request, 'auth_module/loginuser.html', loginuserData)
        else:
            login(request, user)
            return redirect('home')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')