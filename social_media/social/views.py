from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post


def home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "social/home.html", {"posts": posts})


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "social/signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect("home")

    return render(request, "social/signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "social/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "social/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Post.objects.create(
                author=request.user,
                content=content
            )

        return redirect("home")

    return render(request, "social/create_post.html")


@login_required
def like_post(request, id):
    post = Post.objects.get(id=id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("home")


@login_required
def add_comment(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        content = request.POST.get("content")

        if content:
            from .models import Comment
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

    return redirect("home")
