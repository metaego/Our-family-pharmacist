from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import Survey1Form, Survey2Form, Survey3Form, ProfileInfo
from users.models import User, Profile, Survey, SurveyAllergy, SurveyDisease, SurveyFunction, AllergyCode


def profile(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        return redirect('/profiles/survey-1/')
    return render(request, 'profiles/profile.html')

# 전체 프로필 모두 보여주는 화면
# def profile_list(request):
#     profiles = Profile.objects.order_by('-pk')
#     profile_count = profiles.count()
#     context = {'profiles': profiles}
#     return render(request, 'profiles/profile.html')


def survey1(request):
    user_id = request.session.get('custom_user_id')
    # user = User.objects.get(pk=profile_id)
    # request.session['user'] = user.user_id
    if request.method == 'POST':
        form = Survey1Form(request.POST)
        if form.is_valid():
            new_profile=Profile.objects.create()
            profile_id = new_profile.id
            request.session['profile'] = profile_id
            
            survey = Survey()
            survey.user = user_id
            survey.profile = profile_id
            survey.survey_age_group = form.cleaned_data['birth']
            survey.survey_sex = form.cleaned_data['sex']
            survey.survey_pregnancy_code = form.cleaned_data['pregnancy']
            survey.save()

            survey_allergy = SurveyAllergy()
            survey_allergy.allergy_code = form.cleaned_data['allergy']
            survey_allergy.save()

            return redirect('/profiles/survey-2/')            

    else:
        form = Survey1Form()
    context = {'form': form}
    return render(request, 'profiles/survey1.html', context)


# def survey1(request):
#     # user_id = request.session.get('user')
#     # profile_id = request.session.get('profile')
#     if request.method == 'POST':
#         form = Survey1Form(request.POST)
#         if form.is_valid():
#             new_profile = Profile.objects.create()
#             survey = Survey()
#             survey.user_id = User.objects.get(custom_user_id=request.session.get('user'))
#             survey.profile_id = Profile.objects.get(profile_id=new_profile.id)
#             survey.survey_age_group = form.cleaned_data['birth']
#             survey.survey_sex = form.cleaned_data['sex']
#             survey.survey_pregnancy_code = form.cleaned_data['pregnancy']
#             survey.save()

#             survey_allergy = SurveyAllergy()
#             survey_allergy.allergy_code = AllergyCode.objects.get(allergy_code=form.cleaned_data['allergy'])
#             survey_allergy.save()

#             return redirect('/profiles/survey-2/') 
#     else:
#         form = Survey1Form()
#     context = {'form': form}
#     return render(request, 'profiles/survey1.html', context)



# def survey1(request):
#     user_id = request.session.get('user')
#     profile_id = request.session.get('profile')
#     if request.method == 'POST':
#         form = Survey1Form(request.POST)
#         if form.is_valid():
#             if not profile_id:
#                 if user_id:
#                     new_profile = Profile.objects.create(user_id=user_id, profile_birth=form.cleaned_data['birth'])
#                     # new_profile = Profile.objects.create(user_id=user_id, profile_birth=form.cleaned_data['birth'])
#                     profile_id = new_profile.pk
#                     request.session['profile'] = profile_id
#                 else:
#                     # 로그인되지 않은 사용자의 경우 예외 처리
#                     return redirect('/')
#             user_instance = User.objects.get(pk=user_id)
#             profile_instance = Profile.objects.get(pk=profile_id)
#             profile = Profile()
#             profile.user_id = user_instance
#             profile.profile_name = form.cleaned_data['nickname']
#             profile.profile_birth = form.cleaned_data['birth']
#             profile.save()
            
#             survey = Survey()
#             survey.user_id = user_instance.pk
#             survey.profile_id = profile_instance.pk
#             # survey.survey_age_group = form.cleaned_data['birth']
#             survey.survey_sex = form.cleaned_data['sex']
#             survey.survey_pregnancy_code = form.cleaned_data['pregnancy']
#             survey.save()

#             # survey_allergy = SurveyAllergy()
#             # survey_allergy.allergy_code = form.cleaned_data['allergy']
#             # survey_allergy.save()

#             allergy_codes = form.cleaned_data['allergy']
#             for allergy_code in allergy_codes:
#                 allergy_instance = SurveyAllergy.objects.get(allergy_code_id=allergy_code)
#                 survey_allergy = SurveyAllergy.objects.create(allergy_code=allergy_instance)

#             return redirect('/profiles/survey-2/')            

#     else:
#         form = Survey1Form()
#     context = {'form': form}
#     return render(request, 'profiles/survey1.html', context)



def survey2(request):
    if request.method == 'POST':
        form = Survey2Form(request.POST)
        if form.is_valid():
            survey_function = SurveyFunction()
            survey_function.function_code = form.cleaned_data['function'].getlist()
            survey_function.save()

            return redirect('/profiles/survey-3/')            

    else:
        form = Survey1Form()
    context = {'form': form}
    return render(request, 'profiles/survey2.html', context)


def survey3(request):
    if request.method == 'POST':
        form = Survey3Form(request.POST)
        if form.is_valid():
            survey = Survey()
            survey.survey_height = form.cleaned_data['height']
            survey.survey_weight = form.cleaned_data['weight']
            survey.survey_smoke = form.cleaned_data['height']
            survey.survey_alcohol_code = form.cleaned_data['weight']
            survey.save()
            survey_disease = SurveyDisease()
            survey_disease.disease_code = form.cleaned_data['disease']
            survey_disease.save()

            return redirect('/profiles')            

    else:
        form = Survey3Form()
    context = {'form': form}
    return render(request, 'profiles/survey3.html', context)



def profile_info(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    form = ProfileInfo()
    context = {'profile': profile, 'form': form}
    return render(request, 'profiles/profile_info.html', context)


def profile_delete(request):
    return redirect('/profiles')