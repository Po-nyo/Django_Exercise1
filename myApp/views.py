from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Create your views here.


def helloworld(request):
    return render(request, 'helloworld.html')


def post_list(request):
    posts = Post.objects.all().order_by('-created_date')

    return render(request, 'post_list.html', {
        'posts': posts
    })


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
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
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('/')
    else:
        form = PostForm(instance=post)

    return render(request, 'create_post.html', {
        'form': form
    })


def post_remove(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('/')


def sign_up(request):
    return redirect('/')


def login(request):
    return redirect('/')