from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

    return render(request, 'accounts/login.html')

def logout_page(request):

    logout(request)

    return redirect('/login/')  

def register_page(request):

    if request.method == "POST":

        username = request.POST.get('username')

        password = request.POST.get('password')

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'accounts/register.html')