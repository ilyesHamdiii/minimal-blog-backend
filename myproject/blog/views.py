from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from . import models 

def test(request):
    return render(request, "blog/base.html")

def login_view(request):
    if request.method == "POST":
        name = request.POST.get('uname')
        password = request.POST.get('upassword')
        userr = authenticate(request, username=name, password=password)
        if userr is not None:
            auth_login(request, userr) 
            return redirect('/home')
        else:
            return redirect('/login')

    return render(request, "blog/login.html")

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('umail')
        password = request.POST.get('upassword')
        newUser = User.objects.create_user(username=name, email=email, password=password)
        newUser.save()
        return redirect('/login')
    return render(request, "blog/signup.html")

def home(request):
    context = {
        "posts": Post.objects.all(),
    }
    return render(request, "blog/home.html", context)
@login_required
def newpost(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        npost = models.Post(title=title, content=content, author=request.user)
        npost.save()
        return redirect('/home')
    else:
        return render(request, "blog/newpost.html")
@login_required
def mypost(request):
    context = {"posts": Post.objects.filter(author=request.user)}
    return render(request, 'blog/mypost.html', context)
@login_required
def signout(request):
    logout(request)
    return redirect("/login")  
@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author != request.user:
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/mypost')

    return render(request, 'blog/editpost.html', {'post': post})
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author != request.user:
        return HttpResponse("Unauthorized", status=401)

    post.delete()
    return redirect('/mypost')
