from django.shortcuts import render, redirect, reverse
from .models import Post
from .forms import PostForm, UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .token import activation_token

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
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('/')
    else:
        if not request.user.is_authenticated:
            messages.info(request, "로그인이 필요합니다.")
            return redirect('sign_in')
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

    if not request.user.is_authenticated:
        messages.info(request, "로그인이 필요합니다.")
        return redirect('sign_in')

    if post.user != request.user:
        messages.info(request, "권한이 없습니다.")
        return redirect('/')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.info(request, "글이 수정되었습니다.")
            return redirect('/')
    else:
        form = PostForm(instance=post)

    return render(request, 'create_post.html', {
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


def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.create_user(username=user.username,
                                     password=user.password,
                                     is_active=0,
                                     email=user.email,
                                     last_name=user.last_name)

            user = User.objects.get(username=user.username)

            message = render_to_string('activation.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'u_id': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user),
            })

            email = EmailMessage("이메일 인증", message, to=[user.email])
            email.send()

            return redirect(reverse('sign_up_confirm', kwargs={'email': user.email}))

        return redirect('/')
    else:
        form = UserForm()
    return render(request, 'sign_up.html', {
        'form': form,
    })


def sign_up_confirm(request, email):
    return render(request, 'sign_up_confirm.html', {
        'email': email,
    })


def sign_in(request):
    if request.method == 'POST':
        u_id = request.POST['u_id']
        u_pw = request.POST['u_pw']
        user = authenticate(request, username=u_id, password=u_pw)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "로그인에 실패했습니다.")
            return redirect('sign_in')
    else:
        return render(request, 'sign_in.html')


def sign_out(request):
    logout(request)
    messages.info(request, '로그아웃 되었습니다.')
    return redirect('/')


def activate(request, encoded, token):
    u_id = force_text(urlsafe_base64_decode(encoded))
    user = User.objects.get(pk=u_id)
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.info(request, '인증이 완료되었습니다.')
        return redirect('/')
    return redirect('/')


def my_page(request):
    if not request.user.is_authenticated:
        messages.info(request, "로그인이 필요합니다.")
        return redirect('sign_in')

    return render(request, 'my_page.html')
