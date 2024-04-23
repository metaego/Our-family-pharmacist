from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "ex. pharm@ourfamvita.ac"}
        )
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "4자리 이상 입력해 주세요"}
        )
    )

class SignupForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "ex. pharm@ourfamvita.ac"}
        )
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "4자리 이상 입력해 주세요"}
        )
    )
    re_password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "한 번 더 입력해 주세요"}
        )
    )