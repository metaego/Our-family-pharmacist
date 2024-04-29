from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from users.models import User
# from django.contrib.auth.hashers import make_password, check_password

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/profiles/')
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["user_email"]
            user_password = form.cleaned_data["user_password"]

            users = User.objects.filter(custom_user_email=user_email)
            if not users.exists():
                form.add_error("user_email", "등록되지 않은 사용자입니다.")
            else:
                user = users.first()
                if user_password == user.custom_user_password:
                    login(request, user)
                    request.session["user_id"] = user.custom_user_id
                    return redirect("/profiles")
                else:
                    form.add_error("user_password", "비밀번호가 유효하지 않습니다.")
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, "users/login.html", context)


def signout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            user.custom_user_status = 'deactivate'
            user.save()
            return redirect('/')
        else:
            return redirect('/profiles/')
    else:
        return redirect('/')
        # user = User.objects.get(custom_user_id=user_id)
        # user.custom_user_status = 'deactivate'
        # user.save()
        # return redirect('/')


def logout_view(request):
    logout(request)
    return redirect("/")


def signup(request):    
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["user_email"]
            user_password = form.cleaned_data["user_password"]
            re_password = form.cleaned_data["re_password"]

        if User.objects.filter(custom_user_email=user_email).exists():
                form.add_error("user_email", "중복된 이메일입니다.")
        
        elif user_password != re_password:
                form.add_error("re_password", "비밀번호가 일치하지 않습니다.")

        if form.errors:
            context={"form": form}
            return render(request, "users/signup.html", context)
        
        else:
            user = User(custom_user_email=user_email, custom_user_password=user_password)
            user.save()
            login(request, user)
        return redirect("/")

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