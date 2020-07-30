from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def helloworld(request):
    return render(request, 'helloworld.html')


def post_list(request):
    posts = Post.objects.all().order_by('-created_date')

    return render(request, 'post_list.html', {
        'posts': posts
    })


def create_post(request, user_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = User.objects.get(id=user_id)
            post.save()
        return redirect('/')
    else:
        if not request.user.is_authenticated:
            return redirect('/sign_in')
        form = PostForm()
    return render(request, 'create_post.html', {
        'form': form,
    })


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'post_detail.html', {
        'post': post,
    })


def post_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('/sign_in')

    post = Post.objects.get(pk=pk)
    if post.user != request.user:
        return redirect('/')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/')
    else:
        form = PostForm(instance=post)

    return render(request, 'create_post.html', {
        'form': form
    })


def post_remove(request, pk):
    if not request.user.is_authenticated:
        return redirect('/sign_in')
    post = Post.objects.get(pk=pk)
    if post.user != request.user:
        return redirect('/')
    post.delete()
    return redirect('/')


def sign_up(request):
    return redirect('/')


def sign_in(request):
    if request.method == 'POST':
        u_id = request.POST['u_id']
        u_pw = request.POST['u_pw']
        user = authenticate(request, username=u_id, password=u_pw)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "로그인에 실패했습니다.")
            return redirect('/sign_in')
    else:
        return render(request, 'sign_in.html')


def sign_out(request):
    logout(request)
    return redirect('/')
