from django.contrib.auth import login, logout
# from django.contrib.auth.hashers import check_password
# from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import LoginForm, SignupForm, ChangePasswordForm
from users.models import User, Profile
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
            user = User.objects.get(custom_user_email=user_email)
            if (user_email != user.custom_user_email) or (user.custom_user_status == 'deactivate'):
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
    user_id = request.session.get('user')
    print(f'user_id: {user_id}')
    if not user_id:
        return redirect('/')
    
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(custom_user_id=user_id)
            if form.cleaned_data['new_password'] != form.cleaned_data['confirm_password']:
                form.add_error('confirm_password', '비밀번호를 확인해 주세요')
            else:
                user.custom_user_password = form.cleaned_data['confirm_password']
                user.save()
                return redirect('/users/logout/')
    else:
        form = ChangePasswordForm()
    context = {"form": form}
    return render(request, "users/acc_info.html", context)


def signout(request, user_id):
    print(f'user1: {user_id}')
    if request.method == 'POST':
        # URL에서 전달된 user_id 사용
        user = get_object_or_404(User, pk=user_id)
        # user = get_object_or_404(User, pk=user_id)
        print(f'user2: {user_id}')
        user.custom_user_status = 'deactivate'
        user.save()
        return redirect('/')
    
    # else:
    #     return redirect('/profiles/')
    # else:
    #     return redirect('/')
        # user = User.objects.get(custom_user_id=user_id)
        # user.custom_user_status = 'deactivate'
        # user.save()
        # return redirect('/')