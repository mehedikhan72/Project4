from locale import currency
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post, Comment


def index(request):
    if request.user.is_authenticated:
        current_user = request.user.username
    try:
        user = User.objects.filter(username=current_user).values().get()
        id = user["id"]
        posts_lbtcu = Post.objects.filter(likes=id).values() # lbtcu = liked by the current user.
        posts_lbtcu_id = []
        for post in posts_lbtcu:
            posts_lbtcu_id.append(post["id"])

    except UnboundLocalError:
        posts_lbtcu_id = None

    return render(request, "network/index.html", {
        "posts" : Post.objects.all(),
        "posts_lbtcu_id" : posts_lbtcu_id
    })

@login_required
def create_post(request):
    # Getting the username of the current user online
    if request.user.is_authenticated:
        current_user = request.user.username

    if request.method == "POST":
        post = request.POST.get("post")
        if not post:
            return render(request, "network/error.html",{
                "message" : "your post must not be emply."
            })

        # Add post
        p = Post.objects.create(post=post, creator=current_user)
        p.save()

        # Returning to all posts(index)
        return HttpResponseRedirect(reverse("index"))
    
def comments(request, id):
    post = Post.objects.filter(id=id).values().get()
    try:
        comments = Comment.objects.filter(original_post=id).values()
    except Comment.DoesNotExist:
        comments = None
    # print(post)
    # print(comments)
    return render(request, "network/comments.html",{
        "post" : post,
        "comments" : comments,
    })
    pass

@login_required
def create_comment(request, id):
    # Getting the info of the current post where the user is trying to comment on.
    post = Post.objects.filter(id=id).values().get()

    if request.user.is_authenticated:
        current_user = request.user.username

    if request.method == "POST":
        comment = request.POST.get("comment")
        if not comment:
            return render(request, "network/error.html",{
                "message" : "your comment must not be emply."
            })
        
        c = Comment.objects.create(comment=comment, creator=current_user, original_post=post["id"])
        c.save()

        return HttpResponseRedirect(reverse("comments", args=(post["id"],)))

    pass

@login_required
def profile(request, username):

    profile_user = User.objects.filter(username=username)[0]
    posts = Post.objects.filter(creator=username).values()
    
    f = User.objects.get(username=username)
    f1 = f.following.all()
    f2 = f.followers.all()
    
    print(f1)
    print(f2)

    return render(request, "network/profile.html", {
        "profile_user" : profile_user,
        "posts" : posts
    })

@login_required
def follow_toggle(request, username):
    profile_owner_obj = User.objects.get(username=username)
    current_user_obj = request.user
    following = profile_owner_obj.following.all()

    if username != current_user_obj.username:
        if current_user_obj in following:
            profile_owner_obj.following.remove(current_user_obj.id)
        else:
            profile_owner_obj.following.add(current_user_obj.id)
    
    return HttpResponseRedirect(reverse('profile', args=[profile_owner_obj.username]))

def increase_likes(request, id):
    if request.user.is_authenticated:
        current_user = request.user.username
    user = User.objects.filter(username=current_user).values().get()
    user_id = user["id"]
    Post.objects.get(id=id).likes.add(user_id)
    p = Post.objects.get(id=id)
    p.likes_count = p.likes_count + 1
    p.save()

    return HttpResponseRedirect(reverse("index"))

def decrease_likes(request, id):
    if request.user.is_authenticated:
        current_user = request.user.username
    user = User.objects.filter(username=current_user).values().get()
    user_id = user["id"]
    Post.objects.get(id=id).likes.remove(user_id)
    p = Post.objects.get(id=id)
    p.likes_count = p.likes_count - 1
    p.save()
    
    return HttpResponseRedirect(reverse("index"))

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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
