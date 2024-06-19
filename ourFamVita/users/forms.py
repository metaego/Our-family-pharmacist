from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from users.models import User



class LoginForm(forms.Form):
    username = forms.EmailField(label="E-mail",
                                 widget=forms.EmailInput(attrs={"placeholder": "ex. user@pillsogood.com"}))
    password = forms.CharField(label="비밀번호", 
                                    min_length=4, 
                                    widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))



class SignupForm(forms.Form):
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"placeholder": "ex. user@pillsogood.com"}))
    password = forms.CharField(label="비밀번호", min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))
    re_password = forms.CharField(label="비밀번호 재확인", min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "한 번 더 입력해 주세요"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(f'{username}은 중복된 이메일입니다.')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        re_password = self.cleaned_data['re_password']
        if password != re_password:
            self.add_error('re_password', '비밀번호가 일치하지 않습니다.')

    def signup(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = User.objects.create_user(
            username=username,
            password=password
        )
        return user



class AccInfoForm(forms.Form):
    new_password = forms.CharField(label="새로운 비밀번호", widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))
    confirm_password = forms.CharField(label="새로운 비밀번호 확인", widget=forms.PasswordInput(attrs={"placeholder": "한 번 더 입력해 주세요"}))

    def clean(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']
        if new_password != confirm_password:
            self.add_error('confirm_password', '새로운 비밀번호가 일치하지 않습니다.')