from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import Survey1Form, Survey2Form, Survey3Form, ProfileInfo
from users.models import User, Profile, Survey, SurveyAllergy, SurveyDisease, SurveyFunction, AllergyCode, FunctionCode, DiseaseCode


def profile(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'profiles/profile.html', context)


def survey1(request):
    if request.method == 'POST':
        form = Survey1Form(request.POST)
        if form.is_valid():
            user_id = request.session.get('user_id')
            user = User.objects.get(pk=user_id)

            profile = Profile()
            profile.profile_name = form.cleaned_data['nickname']
            profile.profile_birth = form.cleaned_data['birth']
            profile.custom_user_id = user
            profile.save()

            # 프로필ID를 세션에 저장
            request.session["profile_id"] = profile.profile_id

            profile_id = request.session.get('profile_id')
            profile = Profile.objects.get(pk=profile_id)

            survey = Survey()
            survey.custom_user_id = user
            survey.profile_id = profile
            survey.survey_sex = form.cleaned_data['sex']
            survey.survey_pregnancy_code=form.cleaned_data['pregnancy']
            survey.save()

            # 서베이ID를 세션에 저장
            request.session["survey_id"] = survey.survey_id

            survey_id = request.session.get('survey_id')
            survey = Survey.objects.get(pk=survey_id)

            allergy_codes = form.cleaned_data['allergy']
            for allergy_code in allergy_codes:
                allergy_instance = AllergyCode.objects.get(allergy_code=allergy_code)
                SurveyAllergy.objects.create(
                    survey_id=survey,
                    allergy_code=allergy_instance
                )
            return redirect('/profiles/survey-2/')
    else:
        form = Survey1Form()
    context = {'form': form}
    return render(request, 'profiles/survey1.html', context)


def survey2(request):
    if request.method == 'POST':
        form = Survey2Form(request.POST)
        if form.is_valid():
            # 유저, 프로필, 서베이 세션 가져오기
            user_id = request.session.get('user_id')
            profile_id = request.session.get('profile_id')
            survey_id = request.session.get('survey_id')
            
            survey = Survey.objects.get(pk=survey_id)
            function_codes = form.cleaned_data['function']
            
            for function_code in function_codes:
                if len(function_codes) <= 5:              
                    # 기본키가 동작하는 AllergyCode에 넣고 >> 외래키가 동작하는 SurveyAllergy에 넣기
                    function_instance = FunctionCode.objects.get(function_code=function_code)
                    print(f'function_codes={function_codes}')
                    print(f'function_code={function_code}')
                    print(f'function_instance={function_instance}')
                    SurveyFunction.objects.create(
                        survey_id=survey,
                        function_code=function_instance
                    )
                    return redirect('/profiles/survey-3/')
                else:
                    form.add_error("function", "최대 선택 수를 초과하였습니다.")
                    context = {'form': form}
                    return render(request, 'profiles/survey2.html', context)
    else:
        form = Survey2Form()
    context = {'form': form}
    return render(request, 'profiles/survey2.html', context)


def survey3(request):
    if request.method == 'POST':
        form = Survey3Form(request.POST)
        if form.is_valid():
            user_id = request.session.get('user_id')
            profile_id = request.session.get('profile_id')
            survey_id = request.session.get('survey_id')
            print(f'user_id={user_id}')
            print(f'user_id={profile_id}')
            print(f'user_id={survey_id}')
            survey = Survey()
            survey.survey_height = form.cleaned_data['height']
            survey.survey_weight = form.cleaned_data['weight']
            survey.survey_smoke = form.cleaned_data['height']
            survey.survey_alcohol_code = form.cleaned_data['weight']
            survey.save()

            survey = Survey.objects.get(pk=survey_id)            
            disease_codes = form.cleaned_data['disease']
            
            for disease_code in disease_codes:
                if len(disease_codes) <= 5:              
                    # 기본키가 동작하는 DiseaseyCode에 넣고 >> 외래키가 동작하는 SurveyDisease에 넣기
                    disease_instance = DiseaseCode.objects.get(disease_code=disease_code)
                    SurveyDisease.objects.create(
                        survey_id=survey,
                        disease_code=disease_instance
                    )
                    return redirect('/profiles/')
                    print(f'disease_code={disease_code}')
                    print(f'disease_codes={disease_codes}')
                else:
                    form.add_error("disease", "최대 선택 수를 초과하였습니다.")
                    context = {'form': form}
                    return render(request, 'profiles/survey3.html', context)
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