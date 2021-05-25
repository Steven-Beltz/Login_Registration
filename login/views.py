from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    
    return render(request, "index.html")
def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context ={
            "user_name" : request.session['user_name']
    }
    return render(request, "success.html", context)
def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        emailAd = request.POST['email']
        passWord = request.POST['password']
        pw_hash = bcrypt.hashpw(passWord.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=firstName, last_name=lastName, email=emailAd, passWord=pw_hash)
        messages.success(request, "successful registration!")
        return redirect("/")
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        logged_user = User.objects.filter(email=email)
        if logged_user:
            logged_user = logged_user[0]
            if bcrypt.checkpw(password.encode(), logged_user.passWord.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f'{logged_user.first_name} {logged_user.last_name}'
                return redirect("/success")
            else:
                messages.error(request, "Invalid email/password.")
                return redirect('/')
        else:
            messages.error(request, "Email does not exist.")
        return redirect('/')
    return redirect('/')
def log_out(request):
    request.session.flush()
    return redirect('/')