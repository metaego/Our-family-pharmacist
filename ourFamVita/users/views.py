from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm, AccInfoForm
from users.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required


def login_view(request):
    # request로부터 사용자 정보를 가져온다. (로그인하지 않은 경우 request.user에는 AnonymousUser가 할당)
    # 이미 로그인되어 있는 경우
    if request.user.is_authenticated:
        return redirect('/profiles')

    if request.method == 'POST':
        # LoginForm 인스턴스를 만들고, request.POST를 입력 데이터로 사용한다.
        # else 구문을 보면 GET 요청 시에는 Form 인스턴스 생성 시 data를 전달해주지 않는다는 걸 알 수 있다.
        form = LoginForm(data=request.POST)
        # LoginForm에 전달된 데이터가 유효한 경우
        if form.is_valid():
            # form으로 받아온 username과 password 값을 변수에 할당한다.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # user_email, user_password에 해당하는 사용자가 있는지 검사한다.
            user = authenticate(username=username, password=password)

            # 해당 사용자가 존재한다면
            if user:
                login(request, user)
                return redirect('/profiles')
            else:
                form.add_error('username', '등록되지 않은 사용자입니다.')
        # 로그인에 실패한 경우 다시 LoginForm을 사용한 로그인 페이지 렌더링
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'users/login.html', context)



def logout_view(request):
    logout(request)
    return redirect("/")



def signup(request):
    if request.user.is_authenticated:
        return redirect('/profiles')
    
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        # Form 내부에서 비밀번호 일치 여부 등의 유효성 검사 로직을 모두 마친 상태일 경우
        if form.is_valid():
            user = form.signup()
            login(request, user)
            return redirect("/profiles")
    else:
        form = SignupForm()
    # 1. POST 요청에서 생성된 Form이 유효하지 않은 경우, 즉 에러가 존재하는 경우 에러를 포함한 Form을 렌더링
    # 2. GET 요청 시 빈 Form을 렌더링
    context = {'form': form}
    return render(request, 'users/signup.html', context)



@login_required
def acc_info(request):
    user_id = request.user.user_id
    user = User.objects.get(pk=user_id)

    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        form = AccInfoForm(data=request.POST)
        if form.is_valid():
            user.password = make_password(form.cleaned_data['confirm_password'])
            user.save()
            logout(request)
            return redirect("/")
    else:
        form = AccInfoForm()
    context = {"form": form, "user": user}
    return render(request, "users/acc_info.html", context)



def signout(request, user_id):
    user_id = request.user.user_id
    user = User.objects.get(pk=user_id)
    user.is_active = '0'
    user.save()
    logout(request)
    return redirect('/')