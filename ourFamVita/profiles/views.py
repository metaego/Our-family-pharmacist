from django.shortcuts import render, redirect
from profiles.forms import Survey1Form, Survey2Form, Survey3Form
from users.models import User, Profile, Survey, ComCode, SurveyComCode
from django.contrib.auth.decorators import login_required
from django.db.models import Q



@login_required
def profile(request):
    # 로그인하지 않은 경우 로그인 페이지 이동
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user_id = request.user.user_id
        user = User.objects.get(pk=user_id)
        profiles = Profile.objects.filter(user_id=user_id, profile_status='active')
        profile_count = profiles.count()
        context = {'profiles':profiles, "user": user, "profile_count": profile_count}
    return render(request, 'profiles/profile.html', context)



def profile_delete(request, profile_id):
    if request.method == 'POST':
        profile = Profile.objects.get(profile_id=profile_id)
        profile.profile_status = 'deleted'
        profile.save()
        return redirect('/profiles/')



@login_required
def survey1(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = Survey1Form(request.POST)
        if form.is_valid():
            user_id = request.user.user_id
            user = User.objects.get(pk=user_id)

            profile = Profile()
            profile.profile_name = form.cleaned_data['name']
            profile.profile_birth = form.cleaned_data['birth']
            profile.user_id = user
            profile.save()

            # 프로필ID를 세션에 저장
            request.session["profile_id"] = profile.profile_id
            profile_id = request.session.get('profile_id')
            profile = Profile.objects.get(pk=profile_id)

            survey = Survey()
            survey.user_id = user
            survey.profile_id = profile
            survey.survey_sex = form.cleaned_data['sex']
            survey.survey_age_group = form.age_group()
            survey.survey_pregnancy_code = form.clean_pregnancy()
            survey.survey_allergy_code = form.allergy_json()
            survey.save()

            # 서베이ID를 세션에 저장
            request.session["survey_id"] = survey.survey_id

            # survey_com_code 테이블에 저장
            allergy_codes = form.cleaned_data['allergy']
            for allergy_code in allergy_codes:
                allergy_instance = ComCode.objects.get(com_code=allergy_code)
                SurveyComCode.objects.create(survey_id=survey,
                                             com_code_grp = allergy_instance.com_code_grp,
                                             com_code = allergy_instance)
            return redirect('/profiles/survey-2/')
    else:
        form = Survey1Form()
    context = {'form': form}
    return render(request, 'profiles/survey1.html', context)



@login_required
def survey2(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = Survey2Form(request.POST)
        if form.is_valid():
            # 세션에 저장된 서베이ID 불러오기
            survey_id = request.session.get('survey_id')
            survey = Survey.objects.get(pk=survey_id)

            survey.survey_function_code = form.function_json()
            survey.save()

            # survey_com_code 테이블에 저장
            function_codes = form.function_json().values()
            for rank, function_code in enumerate(function_codes, start=1):
                function_instance = ComCode.objects.get(com_code=function_code)
                if 'HF00' in function_code:
                    SurveyComCode.objects.create(survey_id=survey,
                                            com_code_grp = function_instance.com_code_grp,
                                            com_code = function_instance)
                else:
                    SurveyComCode.objects.create(survey_id=survey,
                                            com_code_grp = function_instance.com_code_grp,
                                            com_code = function_instance,
                                            survey_com_code_rank = rank)
            return redirect('/profiles/survey-3/')
    else:
        form = Survey2Form()
    context = {'form': form} 
    return render(request, 'profiles/survey2.html', context)



@login_required
def survey3(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = Survey3Form(request.POST)
        if form.is_valid():
            # 세션에 저장된 서베이ID 불러오기
            survey_id = request.session.get('survey_id')
            survey = Survey.objects.get(pk=survey_id)

            survey.survey_height = form.cleaned_data['height']
            survey.survey_weight = form.cleaned_data['weight']
            survey.survey_smoking_code = form.cleaned_data['smoke']
            survey.survey_alcohol_code = form.cleaned_data['alcohol']
            survey.survey_operation_code = form.cleaned_data['operation']
            survey.survey_disease_code = form.disease_json()
            survey.save()

            # survey_com_code 테이블에 저장
            disease_codes = form.cleaned_data['disease']
            if not disease_codes:
                disease_codes = ['DI00']
            for disease_code in disease_codes:
                disease_instance = ComCode.objects.get(com_code=disease_code)
                SurveyComCode.objects.create(survey_id=survey,
                                             com_code_grp = disease_instance.com_code_grp,
                                             com_code = disease_instance)
            return redirect('/profiles')
    else:
        form = Survey3Form()
    context = {'form': form}
    return render(request, 'profiles/survey3.html', context)



@login_required
def profile_edit1(request, profile_id):
    profile_instance = Profile.objects.get(pk=profile_id)
    
    # profile_id에 대한 survey가 여러 개 존재할 경우 가장 최근 survey를 가져오는 것으로 수정
    # survey_instance = Survey.objects.get(profile_id=profile_id)
    survey_instance = Survey.objects.filter(profile_id=profile_id).last()

            
    if request.method == 'POST':
        form = Survey1Form(request.POST)
        if form.is_valid():
            form.edit_save(profile_instance, survey_instance)

            # survey_com_code 테이블에 저장
            # SurveyComCode.objects.filter(survey_id=survey, com_code_grp='ALLERGY').delete()
            allergy_codes = form.cleaned_data['allergy']
            for allergy_code in allergy_codes:
                allergy_instance = ComCode.objects.get(com_code=allergy_code)
                SurveyComCode.objects.create(survey_id=survey_instance,
                                             com_code_grp=allergy_instance.com_code_grp,
                                             com_code=allergy_instance)
            return redirect(f'/profiles/{profile_id}/profile-edit-2/')
    else:
        initial_data = {
            'name': profile_instance.profile_name,
            'birth': profile_instance.profile_birth,
            'sex': survey_instance.survey_sex,
            'pregnancy': survey_instance.survey_pregnancy_code,
            'allergy': survey_instance.survey_allergy_code.get('ALLERGY', []),
        }
        print(initial_data)
        form = Survey1Form(initial=initial_data)
    context = {'form': form}
    return render(request, 'profiles/profile_edit1.html', context)



@login_required
def profile_edit2(request, profile_id):
    # profile_id에 대한 survey가 여러 개 존재할 경우 건강기능을 선택하지 않는 경우를 제외하고 가장 최근 survey를 가져오는 것으로 수정
    # 단 건강고민을 선택하지 않은 경우만 survey가 존재할 경우 해당 survey를 가져온다.
    # survey_instance = Survey.objects.get(profile_id=profile_id)
    survey_instance = Survey.objects.filter(
        profile_id=profile_id
    ).filter(
        Q(survey_function_code='{"1st": "HF00"}') | ~Q(survey_function_code='{"1st": "HF00"}')
    ).latest('survey_created_at')

    if request.method == 'POST':
        form = Survey2Form(request.POST)
        if form.is_valid():
            form.edit_save(survey_instance)

            # survey_com_code 테이블에 저장
            # SurveyComCode.objects.filter(survey_id=survey, com_code_grp='HF').delete()
            function_codes = form.function_json().values()
            for rank, function_code in enumerate(function_codes, start=1):
                function_instance = ComCode.objects.get(com_code=function_code)
                SurveyComCode.objects.create(survey_id=survey_instance,
                                             com_code_grp=function_instance.com_code_grp,
                                             com_code=function_instance,
                                             survey_com_code_rank=rank)
            return redirect(f'/profiles/{profile_id}/profile-edit-3/')
    else:
        initial_data = {
            'function1': survey_instance.survey_function_code.get('1st'),
            'function2': survey_instance.survey_function_code.get('2nd'),
            'function3': survey_instance.survey_function_code.get('3rd'),
            'function4': survey_instance.survey_function_code.get('4th'),
            'function5': survey_instance.survey_function_code.get('5th'),
        }
        print(initial_data)
        form = Survey2Form(initial=initial_data)
    context = {'form': form}
    return render(request, 'profiles/profile_edit2.html', context)



@login_required
def profile_edit3(request, profile_id):
    # profile_id에 대한 survey가 여러 개 존재할 경우 가장 최근 survey를 가져오는 것으로 수정
    # survey_instance = Survey.objects.get(profile_id=profile_id)
    survey_instance = Survey.objects.filter(profile_id=profile_id).last()
    
    if request.method == 'POST':
        form = Survey3Form(request.POST)
        if form.is_valid():
            form.edit_save(survey_instance)

            # Update SurveyComCode
            # SurveyComCode.objects.filter(survey_id=survey, com_code_grp='DI').delete()
            disease_codes = form.cleaned_data['disease']
            if not disease_codes:
                disease_codes = ['DI00']
            for disease_code in disease_codes:
                disease_instance = ComCode.objects.get(com_code=disease_code)
                SurveyComCode.objects.create(survey_id=survey_instance,
                                             com_code_grp=disease_instance.com_code_grp,
                                             com_code=disease_instance)
            
            return redirect('/profiles')
    else:
        initial_data = {
            'height': survey_instance.survey_height,
            'weight': survey_instance.survey_weight,
            'smoke': survey_instance.survey_smoking_code,
            'alcohol': survey_instance.survey_alcohol_code,
            'operation': survey_instance.survey_operation_code,
            'disease': survey_instance.survey_disease_code.get('DISEASE', []),
        }
        form = Survey3Form(initial=initial_data)
    context = {'form': form}
    return render(request, 'profiles/profile_edit3.html', context)