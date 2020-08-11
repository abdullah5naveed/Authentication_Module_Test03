from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here.

def home(request):
    return render(request, 'auth_module/home.html')


def signupuser(request):
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
        