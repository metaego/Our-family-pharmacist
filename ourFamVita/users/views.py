from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
# from models import User

def login(request):
    if request.user.is_authenticated:
        return redirect("/profiles")

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("/profiles")
            else:
                form.add_error(None, "회원가입이 필요합니다.")
        
        context = {"form": form,}
        return render(request, "users/login.html", context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)

def logout(request):
    logout(request)
    return redirect("/users/login")

def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            re_password = form.cleaned_data["re_password"]

            # if password != re_password:
            #     form.add_error("re_password", "비밀번호가 일치하지 않습니다")

            # if User.objects.filter(email=email).exists():
            #     form.add_error("email", "중복된 이메일입니다.")
            
            # if form.errors:
            #     context = {"form": form}
            #     return render(request, "users/signup.html", context)
            return redirect("/profiles")
            # else:
            #     user = User.objects.create_user(
            #         email=email,
            #         password=password,
            #     )
            #     login(request, user)
            #     return redirect("/profiles")
            
    else:
        form = SignupForm()
        context = {"form": form}
        return render(request, "users/signup.html", context)


def acc_info(request):
    form = PasswordChangeForm()
    context = {"form": form}
    return render(request, "users/acc_info.html", context)