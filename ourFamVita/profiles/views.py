from django.shortcuts import render, redirect

def profile(request):
    return render(request, 'profiles/profile.html')

def survey1(request):
    return render(request, "profiles/survey1.html")

def survey2(request):
    return render(request, "profiles/survey2.html")

def survey3(request):
    return render(request, "profiles/survey3.html")

def profile_info(request):
    return render(request, "profiles/profile_info.html")

def profile_delete(request):
    return redirect("/profiles")