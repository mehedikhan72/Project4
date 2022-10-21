from ast import Delete
from locale import currency
# from xxlimited import new
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers import serialize
import json

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

    posts = Post.objects.all().order_by('-id')

    # Using paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts" : posts,
        "posts_lbtcu_id" : posts_lbtcu_id,
        "page_obj" : page_obj
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
def following_posts(request):
    current_user = request.user.username

    u = User.objects.get(username=current_user)
    f = u.following.all()
    following_list = []

    for user in f:
        following_list.append(user.username)

    posts = Post.objects.filter(creator__in=following_list).order_by('-id')

    # Using paginator
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html",{
        "posts" : posts,
        "following_list" : following_list,
        "page_obj" : page_obj
    })

@login_required
def profile(request, username):

    profile_user = User.objects.filter(username=username)[0]
    posts = Post.objects.filter(creator=username).values().order_by('-id')
    
    # f = User.objects.get(username=username)
    # f1 = f.followers.all()
    # f2 = f.following.all()
    
    # print(f1)
    # print(f2)

    # Using paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile_user" : profile_user,
        "posts" : posts,
        "page_obj" : page_obj
    })

@login_required
def follow_toggle(request, username):
    profile_owner_obj = User.objects.get(username=username)
    current_user_obj = request.user
    followers = profile_owner_obj.followers.all()

    if username != current_user_obj.username:
        if current_user_obj in followers:
            profile_owner_obj.followers.remove(current_user_obj.id)
        else:
            profile_owner_obj.followers.add(current_user_obj.id)
    
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


# This function is to fetch data for editing a post
def particular_post(request, id):
    post = Post.objects.filter(id=id)
    post_data = serialize("json", post)
    return HttpResponse(post_data, content_type="application/json")

def save_edited_post(request, id):
    new_post_content = json.load(request)['new_post_content']
    print(new_post_content)

    p = Post.objects.get(id=id)
    p.post = new_post_content
    p.save()

    post = Post.objects.filter(id=id)
    post_data = serialize("json", post)
    
    return HttpResponse(post_data, content_type="application/json")



