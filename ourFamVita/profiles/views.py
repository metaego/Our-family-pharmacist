from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import Survey1Form, Survey2Form, Survey3Form, ProfileInfo
from users.models import Profile, Survey, SurveyAllergy, SurveyDisease, SurveyFunction


# 전체 프로필 모두 보여주는 화면
def profile(request):
    profiles = Profile.objects.order_by("-pk")
    profile_count = profiles.count()
    context = {"profiles": profiles}
    return render(request, 'profiles/profile.html')


def survey1(request):
    if request.method == "POST":
        form = Survey1Form(request.POST)
        if form.is_valid():
            profile_id = request.session.get("profile")
            profile = Profile.objects.get(pk=profile_id)
            survey = Survey()
            survey.profile_id = profile
            survey.survey_age_group = form.cleaned_data["birth"]
            survey.survey_sex = form.cleaned_data["sex"]
            survey.survey_pregnancy_code = form.cleaned_data["pregnancy"]
            survey.save()

            survey_allergy = SurveyAllergy()
            survey_allergy.allergy_code = form.cleaned_data["allergy"]
            survey_allergy.save()

            return redirect("/profiles/survey-2/")            

    else:
        form = Survey1Form()
    context = {"form": form}
    return render(request, "profiles/survey1.html", context)



def survey2(request):
    if request.method == "POST":
        form = Survey2Form(request.POST)
        if form.is_valid():
            survey_function = SurveyFunction()
            survey_function.profile_id = profile
            survey.survey_age_group = form.cleaned_data["birth"]
            survey.survey_sex = form.cleaned_data["sex"]
            survey.survey_pregnancy_code = form.cleaned_data["pregnancy"]
            survey.save()

            survey_allergy = SurveyAllergy()
            survey_allergy.allergy_code = form.cleaned_data["allergy"]
            survey_allergy.save()

            return redirect("/profiles/survey-2/")            

    else:
        form = Survey1Form()
    context = {"form": form}
    return render(request, "profiles/survey2.html", context)


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
    context = {"profile": profile, "form": form}
    return render(request, "profiles/profile_info.html", context)


def profile_delete(request):
    return redirect("/profiles")