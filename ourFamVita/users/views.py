from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from users.models import User
# from django.contrib.auth.hashers import make_password, check_password

def login_view(request):
    user_id = request.session.get('user')
    if user_id:
        return redirect('/profiles')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_email = request.POST.get('user_email', None)
            user_password = request.POST.get('user_password', None)

            if not (user_email and user_password):
                form.add_error(None, '모든 값을 입력해야 합니다.')
            else:
                user = User.objects.get(custom_user_email=user_email)
                print(user)
                if not user_email == user.custom_user_email:
                    form.add_error('user_email', '등록되지 않은 사용자입니다.')
                    # print(request.session['user'])
                else:
                    if user_password == user.custom_user_password:
                        request.session['user'] = user.custom_user_id
                        return redirect('/profiles')
                    else:
                        form.add_error('user_password', '비밀번호가 유효하지 않습니다.')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'users/login.html', context)

    # print(request.user)
    # if request.user.is_authenticated:
    #     return redirect('/profiles/')
    
    # if request.method == "POST":
    #     form = LoginForm(data=request.POST)
    #     if form.is_valid():
    #         # user_email = form.cleaned_data["user_email"]
    #         # user_password = form.cleaned_data["user_password"]

    #         user_email = request.POST.get('user_email', None)
    #         user_password = request.POST.get('user_password', None)

    #         users = User.objects.filter(custom_user_email=user_email)
    #         print(users)
    #         print(user_email)
    #         print(request.POST.get('user'))

    #         if not users.exists():
    #             form.add_error("user_email", "등록되지 않은 사용자입니다.")
    #         else:
    #             user = users.first()
    #             print(user)

    #             if user_password == user.custom_user_password:
    #                 login(request, user)
    #                 request.session["user_id"] = user.custom_user_id
    #                 print(user.custom_user_id)


    #                 return redirect("/profiles")
    #             else:
    #                 form.add_error("user_password", "비밀번호가 유효하지 않습니다.")
    # else:
    #     form = LoginForm()
    # context = {"form": form}
    # return render(request, "users/login.html", context)


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