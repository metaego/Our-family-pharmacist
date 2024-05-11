from django import forms
from django.core.exceptions import ValidationError
from users.models import User


class LoginForm(forms.Form):
    user_email = forms.CharField(label="E-mail",
                                 widget=forms.TextInput(attrs={"placeholder": "ex. user@pillsogood.com"}))
    user_password = forms.CharField(label="비밀번호", 
                                    min_length=4, 
                                    widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))


class SignupForm(forms.Form):
    user_email = forms.CharField(label="E-mail", widget=forms.TextInput(attrs={"placeholder": "ex. user@pillsogood.com"}))
    user_password = forms.CharField(label="비밀번호", min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))
    re_password = forms.CharField(label="비밀번호 재확인", min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "한 번 더 입력해 주세요"}))