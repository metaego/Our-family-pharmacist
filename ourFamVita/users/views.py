from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
# from ourFamVita.models import User
from users.models import User

def login(request):
    if request.user.is_authenticated:
        return redirect("/profiles/")

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("/profiles/")
            else:
                form.add_error(None, "회원가입이 필요합니다.")
        
        context = {"form": form}
        return render(request, "users/login.html", context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)

def logout(request):
    logout(request)
    return redirect("/users/login/")

def signup(request):    
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/users/login/")
                            
        else:
            context = {"form": form}
            return render(request, "users/signup.html", context)            
            
    else:
        form = SignupForm()
        context = {"form": form}
    return render(request, "users/signup.html", context)


def acc_info(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PasswordChangeForm(user=request.user)

    context = {"form": form}
    return render(request, "users/acc_info.html", context)