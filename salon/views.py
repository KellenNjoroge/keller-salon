from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from peewee import DoesNotExist
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db import transaction


# Create your views here.
def index(request):
    return render(request, 'index.html',)


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    print(profile)
    # profile = Profile.objects.filter(user=request.user.id)

    return render(request, 'profile.html', {'profile': profile,})


def update(request):
    # current_user = User.objects.get(pk=user_id)
    current_user = request.user
    if request.method == 'POST':
        user_form = EditUser(request.POST, request.FILES, instance=request.user)
        profile_form = EditProfile(request.POST, request.FILES, instance=current_user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
        return redirect('profile')

    else:
        user_form = EditUser(instance=request.user)
        profile_form = EditProfile(instance=current_user.profile)
    return render(request, 'update_profile.html', {
        "user_form": user_form,
        "profile_form": profile_form
    })


@login_required(login_url='/accounts/login/')
def town(request, town_id):
    current_user = request.user
    town_name = current_user.profile.town
    # if current_user.profile.hood is None:
    #     return redirect('update')
    # else:
    town = Post.get_town_posts(id=town_id)
    comments = Comment.objects.all()
    form = NewComment(instance=request.user)

    return render(request, 'your_town.html',
                  {'town': town, 'town_name': town_name, 'comments': comments, 'comment_form': form})


@login_required(login_url='/accounts/login/')
def new_town(request):
    current_user = request.user
    town_name = current_user.profile.town
    if request.method == 'POST':
        NewTownForm = NewTown(request.POST)
        if NewTownForm.is_valid():
            townform = NewTownForm.save(commit=False)
            townform.admin = current_user
            current_user.profile.townpin = True
            townform.save()
            print('saved')

            # request.session.modified = True
            # current_user.profile.hood = hoodform.id
        # return redirect('profilehood',hoodform.name)
        return redirect('index')


    else:
        NewTownForm = NewTown()
    return render(request, 'new_town.html', {"newTownForm": NewTownForm,

                                            'town_name': town_name})


def all_towns(request):
    current_user = request.user
    towns = Town.objects.all()

    return render(request, 'all_towns.html', {'towns': towns})


def join(request, id):
    current_user = request.user
    town_name = current_user.profile.town
    town = Town.objects.get(id=id)
    current_user.profile.town = town
    current_user.profile.save()

    return redirect('index')


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    town_name = current_user.profile.hood
    town = request.user.profile.hood
    if request.method == 'POST':
        newPostForm = NewPost(request.POST, request.FILES)
        if newPostForm.is_valid():
            new_post = newPostForm.save(commit=False)
            new_post.poster = request.user
            new_post.town = town
            new_post.save()
        return redirect('index')

    else:
        newPostForm = NewPost()
    return render(request, 'new_post.html', {"newPostForm": newPostForm,
                                            'town_name': town_name})


def comment(request, id):
    post = Post.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        comm = NewComment(request.POST)
        if comm.is_valid():
            comment = comm.save(commit=False)
            comment.commentator = request.user
            comment.comment_post = post
            comment.save()
            return redirect('index')
    return redirect('index')


def exit_town(request, id):
    current_user = request.user
    # hood_name = current_user.profile.hood
    # hood = Hood.objects.get(id=id)
    current_user.profile.town = None
    current_user.profile.save()

    return redirect('index')