from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import re
# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not username.strip() or not email.strip() or not password.strip() or not confirmpassword.strip():
            messages.warning(request, "Avoid the spaces and Enter the values!")
            return render(request, 'signup.html')

        if not re.match(r'^[a-zA-Z0-9]+$', username):
            messages.warning(
                request, "Username should contain only alphanumeric characters.")
            return render(request, 'signup.html')

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('register')
            else:
                user_reg = User.objects.create_user(
                    username=username, email=email, password=password)
                user_reg.save()
                messages.success(request, "Successfully created")
                return redirect('login')
        else:
            messages.error(request, "Password doesn't match")
            return redirect('register')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print('thi reach here ')
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Success")
            return redirect('/')
        else:
            messages.error(request, "Invalid credential")
            return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')
