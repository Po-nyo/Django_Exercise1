from django import forms
from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'last_name']
        labels = {
            'username': '아이디',
            'password': '비밀번호',
            'email': '이메일',
            'last_name': '닉네임',
        }
