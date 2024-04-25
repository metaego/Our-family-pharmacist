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

    def clean_email(self):
        user_email = self.cleaned_data["user_email"]
        if User.objects.filter(user_email=user_email).exists():
            raise ValidationError(f"중복된 이메일입니다.")
        return user_email
    
    def clean(self):
        user_password = self.cleaned_data["user_password"]
        re_password = self.cleaned_data["re_password"]
        if user_password != re_password:
            self.add_error("re_password", "비밀번호가 일치하지 않습니다.")


    # def save(self):
    #     user_email = self.cleaned_data["user_email"]
    #     user_password = self.cleaned_data["user_password"]
    #     user = User(user_email, user_password=user_password)
    #     return user
        # user = User(user_email=email, user_password=password)
        # user.save()