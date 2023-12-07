import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from math import ceil

from .models import User, Post
from .forms import new_post_form


def index(request):
    return render(request, "network/index.html", {
        'new_post_form' : new_post_form,
        'pagination_len' : list(range(1, ceil(len(Post.objects.all())/10) + 1)),
        'pag_len' : ceil(len(Post.objects.all())/10),
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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def submit_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        poster = User.objects.get(id=data.get("poster"))
        post_content = data.get("post")
        post = Post(poster=poster, post=post_content)
        post.save()
        return JsonResponse({"message": "Posted successfully."}, status=201)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        post = Post.objects.get(id=data.get('id'))
        if post.poster == request.user:
            post.post = data.get('content')
            post.save()
            return JsonResponse({'message': 'Post editted successfully'}, status=201)
        else: 
            print('impoater spotted') 
            return JsonResponse({'meassage': 'you are an imposter :('})


def posts(request, page_number):
        posts = Post.objects.all()
        posts = posts.order_by('-timestamp').all()
        result = [post.serialize(request.user) for post in posts]
        result = Paginator(result, 10)
        return JsonResponse(result.page(page_number).object_list, safe=False)

@csrf_exempt
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'GET':
        return render(request, 'network/profile.html', {
            'profile': user,
            'following': User.objects.all().filter(followers=user).count(),
            'followers' : user.followers.count(),
            'is_following': request.user in user.followers.all(),
            'profile_id' : user_id,
            'pagination_len' : list(range(1, ceil(len(Post.objects.filter(poster=user))/10) + 1)),
            'pag_len' : ceil(len(Post.objects.filter(poster=user))/10),
        })
    elif request.method == 'POST':
        print('put request spotted')
        data = json.loads(request.body)
        profile = User.objects.get(id=data.get('profile_id'))
        if data.get('follow') == True:
            profile.followers.add(request.user)
            return HttpResponse('Followed succesfully')
        else:
            profile.followers.remove(request.user)
            return HttpResponse('Unfollowed succesfully')


@login_required
def followig(request):
        return render(request, "network/following.html", {
        'new_post_form' : new_post_form,
        'pagination_len' : list(range(1, ceil(len(Post.objects.filter(poster__in=User.objects.filter(followers=request.user)).all())/10) + 1)),
        'pag_len' : ceil(len(Post.objects.filter(poster__in=User.objects.filter(followers=request.user)).all())/10),
    })


@login_required
def postsfollowing(request, page_number):
        posts = Post.objects.filter(poster__in=User.objects.filter(followers=request.user))
        posts = posts.order_by('-timestamp').all()
        result = [post.serialize(request.user) for post in posts]
        result = Paginator(result, 10)
        return JsonResponse(result.page(page_number).object_list, safe=False)


@csrf_exempt
def like(request):
    data = json.loads(request.body)
    task = data.get('task')
    post = Post.objects.get(id=data.get('post_id'))
    if task == 'like':
        post.liked.add(request.user)
        post.likes += 1
        post.save()
        return JsonResponse({'message': 'liked succefully'})
    else:
        post.liked.remove(request.user)
        post.likes -= 1
        post.save()
        return JsonResponse({'message': 'unliked succesfully'})


@csrf_exempt
def profileposts(request, page_number):
        data = json.loads(request.body)
        poster = User.objects.get(id=data.get('id'))
        posts = Post.objects.filter(poster = poster)
        posts = posts.order_by('-timestamp').all()
        result = [post.serialize(request.user) for post in posts]
        result = Paginator(result, 10)
        return JsonResponse(result.page(page_number).object_list, safe=False)

