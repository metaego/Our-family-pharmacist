from django import forms
from django.core.exceptions import ValidationError
from users.models import User


class LoginForm(forms.Form):
    user_email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ex. pharm@ourfamvita.ac"}))
    user_password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))


class SignupForm(forms.Form):
    user_email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ex. pharm@ourfamvita.ac"}))
    user_password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))
    re_password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "한 번 더 입력해 주세요"}))