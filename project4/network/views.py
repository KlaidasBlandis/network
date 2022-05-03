from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Follower, NewPost, User, UserPage


def index(request):
    posts = NewPost.objects.all()
    return render(request, "network/index.html", {
        "posts": reversed(posts)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        user_page = UserPage(user=user)
        user_page.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request):
    if request.method == "POST":
        user = request.user
        text = request.POST["text"]
        post = NewPost(user=user, text=text)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:    
        return render(request, "network/post.html")

def user_page(request, user_id):
    user = User(pk=user_id)
    user_page = UserPage.objects.get(user=user)

    return render(request, "network/user.html", {
        "user_p": user_page,
        "posts": reversed(NewPost.objects.filter(user=user).all())
    })

def follow(request):
    f = request.GET["f"]
    page_user = request.GET["user"]
    print (page_user)
    follower = request.user
    up = UserPage.objects.get(user=page_user)
    print(up)
    # renders the 1 as a text
    if f == '1':
        followers = up.followers - 1
        UserPage.objects.filter(user=page_user).update(followed=False, followers=followers)
        Follower.objects.update(follower=follower, user_page=False)
    else:
        followers = up.followers + 1
        UserPage.objects.filter(user=page_user).update(followed=True, followers=followers)
        Follower.objects.update(follower=follower, user_page=up)
    return HttpResponseRedirect(reverse("user_page", args=page_user))

def following(request):
    user = request.user
    following = Follower.objects.filter(follower=user)
    return render(request, "network/following.html", {
        "pages": following.user_page
    })
