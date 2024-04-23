from django.shortcuts import render, redirect
from profiles.forms import Survey1Form, Survey3Form, ProfileInfo

def profile(request):
    return render(request, 'profiles/profile.html')

def survey1(request):
    form = Survey1Form()
    context = {"form": form}
    return render(request, "profiles/survey1.html", context)

def survey2(request):
    return render(request, "profiles/survey2.html")

def survey3(request):
    form = Survey3Form()
    context = {"form": form}
    return render(request, "profiles/survey3.html", context)

def profile_info(request):
    if request.method == "POST":
        form = ProfileInfo(request.POST)
        if form.is_valid():
            profile = form.save()
            return redirect("profiles:profile")
    else:
        form = ProfileInfo()
    context = {"form": form}
    return render(request, "profiles/profile_info.html", context)

def profile_delete(request):
    return redirect("/profiles")