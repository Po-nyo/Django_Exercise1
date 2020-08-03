from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'last_name']
        widgets = {'password': forms.PasswordInput}
        labels = {
            'username': '아이디',
            'password': '비밀번호',
            'email': '이메일',
            'last_name': '닉네임',
        }
