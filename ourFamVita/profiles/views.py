from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import Survey1Form, Survey3Form, ProfileInfo
from ourFamVita.models import Profile



def profile(request):
    # if request.method == "POST":
    #     form = ProfileView(request.POST)
    #     if form.is_valid():
    #         profile = form.save(commit=False)
    #         profile.user = request.users
    #         profile.save()
    #         return redirect('/profiles/profile/')
    # else:
    #     form = ProfileView()
    return render(request, 'profiles/profile.html')

def survey1(request):
    if request.method == "POST":
        form = Survey1Form(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Survey1Form()
    context = {"form": form}
    return render(request, "profiles/survey1.html", context)

def survey2(request):
    return render(request, "profiles/survey2.html")

def survey3(request):
    if request.method == "POST":
        form = Survey3Form(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Survey3Form()
    context = {"form": form}
    return render(request, "profiles/survey3.html", context)

def profile_info(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    form = ProfileInfo()
    # if request.method == "POST":
    #     form = ProfileInfo(request.POST)
    #     if form.is_valid():
    #         profile = form.save()
    #         return redirect("profiles:profile")
    # else:
    #     form = ProfileInfo()
    
    context = {"form": form, "profile": profile}
    return render(request, "profiles/profile_info.html", context)


def profile_delete(request):
    return redirect("/profiles")