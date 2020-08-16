from django.shortcuts import render, redirect
from dash_app.models import *
from django.contrib import messages
import bcrypt

# First page - login and register
def render_log_reg(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.validator(request.POST)
    users = User.objects.filter(email = request.POST['email'])
    if len(users) > 0:
        errors['email_address'] = "This email is already registered!"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()    
        User.objects.create(
            first_name = request.POST['fname'],
            last_name = request.POST['lname'],
            email = request.POST['email'], 
            password=pw_hash,
        ) 
    return redirect("/") 

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['name'] = f"{logged_user.first_name} {logged_user.last_name}"
                request.session['uid'] = logged_user.id
                return redirect('/quotes')
    messages.error(request,"Invalid email or incorrect password!")
    return redirect("/")

# Quotes Dashboard - Add new quote and show all quotes on dashboard
def render_dash(request):
    if 'uid' not in request.session :
        return redirect('/')
    context = {
        "quotes" : Quote.objects.all()
    }
    return render(request,'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def post(request):
    if (request.method == "POST"):
        errors = Quote.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/quotes')
        Quote.objects.create(
            author = request.POST['author'],
            content = request.POST['content'],
            poster = User.objects.get(id = request.session['uid']),
        )
        return redirect('/quotes')
    return redirect('/')

def delete(request, id):
    post = Quote.objects.get(id=id)
    post.delete()
    return redirect('/quotes')

def add_like(request, id):
    liked_quote = Quote.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['uid'])
    if liked_quote.poster.id != user_liking.id:
        liked_quote.likes.add(user_liking)
    else:
        messages.error(request,"Can't like your own post.")
    return redirect('/quotes')

# Account page - edit user information
def render_account(request,uid):
    context = {
        "user" : User.objects.get(id=uid)
    }
    return render(request, 'account.html', context)

def update_account(request,uid):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            # return redirect(f'/myaccount/{str(uid)}')
        else:
            users = User.objects.filter(email=request.POST['email'])
            if users: 
                logged_user = users[0]
            user = User.objects.get(id=uid)
            if user == logged_user:
                user.first_name = request.POST['fname']
                user.last_name = request.POST['lname']
                user.email = request.POST['email']
            else:
                messages.error(request,"Email has already taken!")
    return redirect(f'/myaccount/{str(uid)}')

# Profile - show user's all posted quotes
def render_profile(request, uid):
    context = {
        "poster" : User.objects.get(id=uid)
    }
    return render(request,'profile.html',context)