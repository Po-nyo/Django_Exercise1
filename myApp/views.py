from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .visualization import VisualizationFolium, VisualizationPlotly
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Create your views here.


def helloworld(request):
    return render(request, 'myApp/helloworld.html')


def post_list(request):
    all_posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'myApp/post_list.html', {
        'posts': posts
    })


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
        return redirect('/')
    else:
        if not request.user.is_authenticated:
            messages.info(request, "로그인이 필요합니다.")
            return redirect('sign_in')
        form = PostForm()
    return render(request, 'myApp/create_post.html', {
        'form': form,
    })


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'myApp/post_detail.html', {
        'post': post,
    })


def post_edit(request, pk):
    post = Post.objects.get(pk=pk)

    if not request.user.is_authenticated:
        messages.info(request, "로그인이 필요합니다.")
        return redirect('sign_in')

    if post.user != request.user:
        messages.info(request, "권한이 없습니다.")
        return redirect('/')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, "글이 수정되었습니다.")
            return redirect('/')
    else:
        form = PostForm(instance=post)

    return render(request, 'myApp/create_post.html', {
        'form': form
    })


def post_remove(request, pk):
    post = Post.objects.get(pk=pk)

    if not request.user.is_authenticated:
        messages.info(request, "로그인이 필요합니다.")
        return redirect('sign_in')

    if post.user != request.user and not request.user.is_superuser:
        messages.info(request, "권한이 없습니다.")
        return redirect('/')

    post.delete()
    messages.info(request, "게시물을 삭제했습니다.")
    return redirect('/')


def my_page(request):
    if not request.user.is_authenticated:
        messages.info(request, "로그인이 필요합니다.")
        return redirect('sign_in')

    return render(request, 'myApp/my_page.html')


def post_list_by_author(request, username):
    author = User.objects.get(username=username)
    posts = author.posts.all()
    return render(request, 'myApp/post_list.html', {
        'posts': posts,
        'author': author.last_name,
    })


def visualization_service(request):
    if not request.user.is_authenticated:
        messages.info(request, "로그인이 필요합니다.")
        return redirect('sign_in')

    return render(request, 'myApp/visualization_service.html', {
    })


@xframe_options_sameorigin
def visualization_view(request):
    if not request.user.is_authenticated:
        messages.info(request, "로그인이 필요합니다.")
        return redirect('sign_in')

    select = request.GET.get('select')

    if select == 'plt_gapminder':
        figure = VisualizationPlotly().get_gapminder_figure()
        template = 'myApp/visualization/plotly_view.html'
    elif select == 'plt_iris':
        figure = VisualizationPlotly().get_iris_figure()
        template = 'myApp/visualization/plotly_view.html'
    elif select == '푸드트럭_허가구역':
        figure = VisualizationFolium().get_foodtruck_figure()
        template = 'myApp/visualization/folium_view.html'
    else:
        figure = VisualizationFolium().get_figure(select)
        template = 'myApp/visualization/folium_view.html'

    return render(request, template, {
        'figure': figure,
    })
