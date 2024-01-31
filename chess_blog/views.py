from django.shortcuts import render, redirect, get_object_or_404
from .forms import (RegistrationForm, ChessPostForm, AuthenticationFormWithPlaceholder,
                    ChessCommentForm)
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse


def home(request):
    return render(request, 'chess_blog/home.html')


def register_user(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
    return render(request, 'chess_blog/register_user.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationFormWithPlaceholder(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('chess_blog/home.html')
    else:
        form = AuthenticationFormWithPlaceholder()
    return render(request, 'chess_blog/login_user.html', {'form': form})


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ChessPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect('chess_blog/home.html')
    else:
        form = ChessPostForm()

    return render(request, 'chess_blog/add_article.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = ChessPost.objects.get(id=post_id)
    if request.method == 'POST':
        form = ChessCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post', args=[post_id]))
    else:
        form = ChessCommentForm()

    return render(request, 'chess_blog/add_comment.html', {'form': form, 'post': post})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def world_champions(request):
    return render(request, 'chess_blog/world_champions.html')


def strategy(request):
    return render(request, 'chess_blog/strategy.html')


def advices_for_beginners(request):
    return render(request, 'chess_blog/advices_for_beginners.html')


def why_the_chess(request):
    return render(request, 'chess_blog/why_the_chess.html')


def show_post(request, post_id):
    post = get_object_or_404(ChessPost, pk=post_id)
    comments = ChessComment.objects.filter(post=post)
    return render(request, 'chess_blog/post.html', {'post': post, 'comments': comments})


def delete_comment(request, comment_id):
    comment = get_object_or_404(ChessComment, pk=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('post', comment.post.pk)
