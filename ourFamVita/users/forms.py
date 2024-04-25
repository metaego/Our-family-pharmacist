from django import forms
from django.core.exceptions import ValidationError
# from ourFamVita.models import User
from users.models import User

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ex. pharm@ourfamvita.ac"}))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))


class SignupForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ex. pharm@ourfamvita.ac"}))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "4자리 이상 입력해 주세요"}))
    re_password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={"placeholder": "한 번 더 입력해 주세요"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(user_email=email).exists():
            raise ValidationError(f"중복된 이메일입니다.")
        return email
    
    def clean(self):
        password = self.cleaned_data["password"]
        re_password = self.cleaned_data["re_password"]
        if password != re_password:
            self.add_error("re_password", "비밀번호가 일치하지 않습니다.")


    def save(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User.objects.create(
            user_email=email, 
            user_password=password
        )
        return user
        # user = User(user_email=email, user_password=password)
        # user.save()