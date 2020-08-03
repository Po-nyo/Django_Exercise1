from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm
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


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.instance.is_active = False
            User.objects.create_user(username=form.instance.username,
                                     password=form.instance.password,
                                     is_active=form.instance.is_active,
                                     email=form.instance.email,
                                     last_name=form.instance.last_name)

            user = User.objects.get(username=form.instance.username)

            message = render_to_string('accounts/activation.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'u_id': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user),
            })

            email = EmailMessage("이메일 인증", message, to=[user.email])
            email.send()

            return redirect(reverse('sign_up_confirm', kwargs={'email': user.email}))
        else:
            messages.info(request, "사용할 수 없는 ID 입니다.")
            return redirect('sign_up')
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {
        'form': form,
    })


def sign_up_confirm(request, email):
    return render(request, 'accounts/sign_up_confirm.html', {
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
        return render(request, 'accounts/sign_in.html')


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
