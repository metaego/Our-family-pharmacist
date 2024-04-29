from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import Survey1Form, Survey2Form, Survey3Form, ProfileInfo
from users.models import User, Profile, Survey, SurveyAllergy, SurveyDisease, SurveyFunction, AllergyCode, DiseaseCode, FunctionCode


def profile(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    profiles = Profile.objects.filter(custom_user_id=user_id, profile_status='activate')
    profile_count = profiles.count()
    context = {'profiles':profiles, "user": user, "profile_count": profile_count}
    return render(request, 'profiles/profile.html', context)


def profile_delete(request, profile_id):
    if request.method == 'POST':
        profile = Profile.objects.get(profile_id=profile_id)
        profile.profile_status = 'deactivate'
        profile.save()
        return redirect('/profiles/')


def survey1(request):
    if request.method == 'POST':
        form = Survey1Form(request.POST)
        if form.is_valid():
            user_id = request.session.get('user_id')
            user = User.objects.get(pk=user_id)

            profile = Profile()
            profile.profile_name = form.cleaned_data['name']
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
            survey_id = request.session.get('survey_id')            
            survey = Survey.objects.get(pk=survey_id)

            function_codes = form.cleaned_data['function']
            if not function_codes:
                return redirect('/profiles/survey-3/')
            for function_code in function_codes:
                if len(function_codes) <= 5:              
                    # 기본키가 동작하는 AllergyCode에 넣고 >> 외래키가 동작하는 SurveyAllergy에 넣기
                    function_instance = FunctionCode.objects.get(function_code=function_code)
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
            user = User.objects.get(pk=user_id)

            profile_id = request.session.get('profile_id')
            profile = Profile.objects.get(pk=profile_id)         

            survey = Survey()
            survey.custom_user_id = user
            survey.profile_id = profile
            survey.survey_height = form.cleaned_data['height']
            survey.survey_weight = form.cleaned_data['weight']
            survey.survey_smoke = form.cleaned_data['smoke']
            survey.survey_alcohol_code = form.cleaned_data['alcohol']
            survey.save()

            survey_id = request.session.get('survey_id')
            survey = Survey.objects.get(pk=survey_id)   

            disease_codes = form.cleaned_data['disease']
            if not disease_codes:
                return redirect('/profiles/')
            for disease_code in disease_codes:
                if len(disease_codes) <= 5:              
                    # 기본키가 동작하는 DiseaseyCode에 넣고 >> 외래키가 동작하는 SurveyDisease에 넣기
                    disease_instance = DiseaseCode.objects.get(disease_code=disease_code)
                    SurveyDisease.objects.create(
                        survey_id=survey,
                        disease_code=disease_instance
                    )
                  
                    return redirect('/profiles/')
                else:
                    form.add_error("disease", "최대 선택 수를 초과하였습니다.")
                    context = {'form': form}
                    return render(request, 'profiles/survey3.html', context)
    else:
        form = Survey3Form()
    context = {'form': form}
    return render(request, 'profiles/survey3.html', context)



def profile_info(request, profile_id):
    profile_edit = Profile.objects.get(pk=profile_id)
    if request.method == 'POST':
        form = ProfileInfo(request.POST)
        if form.is_valid():
            # 유저 ID 불러오기
            user_id = request.session.get('user_id')
            user = User.objects.get(pk=user_id)

            # 프로필 DB 가져오기
            profile_edit.profile_name = form.cleaned_data['name']
            profile_edit.profile_birth = form.cleaned_data['birth']
            # profile_edit.custom_user_id = user
            profile_edit.save()

            # # 프로필 ID를 세션에 저장
            # request.session["profile_id"] = profile.profile_id
            # # 프로필 ID 불러오기
            # profile_id = request.session.get('profile_id')
            # profile = Profile.objects.get(pk=profile_id)

            # 서베이 DB 가져오기
            survey = Survey.objects.get(profile_id=profile_edit)
            survey.survey_sex = form.cleaned_data['sex']
            survey.survey_pregnancy_code=form.cleaned_data['pregnancy']
            survey.survey_height = form.cleaned_data['height']
            survey.survey_weight = form.cleaned_data['weight']
            survey.survey_smoke = form.cleaned_data['smoke']
            survey.survey_alcohol_code = form.cleaned_data['alcohol']
            survey.save()

            # # 서베이 ID를 세션에 저장
            # request.session["survey_id"] = survey.survey_id
            # # 서베이 ID 불러오기
            # survey_id = request.session.get('survey_id')
            # survey = Survey.objects.get(pk=survey_id)

            # 알레르기 DB에 정보 저장
            allergy_codes = form.cleaned_data['allergy']
            for allergy_code in allergy_codes:
                allergy_instance = AllergyCode.objects.get(allergy_code=allergy_code)
                SurveyAllergy.objects.create(
                    survey_id=survey,
                    allergy_code=allergy_instance
                )

            # 건강고민 DB에 정보 저장
            function_codes = form.cleaned_data['function']
            if not function_codes:
                return redirect('/profiles/')
            if len(function_codes) > 5:
                form.add_error("function", "최대 선택 수를 초과하였습니다.")
            else:
                for function_code in function_codes:
                    function_instance = FunctionCode.objects.get(function_code=function_code)
                    SurveyFunction.objects.create(
                        survey_id=survey,
                        function_code=function_instance
                    )

            # 기저질환 DB에 정보 저장
            disease_codes = form.cleaned_data['disease']
            if not disease_codes:
                return redirect('/profiles/')
            if len(disease_codes) > 5:
                form.add_error("disease", "최대 선택 수를 초과하였습니다.")
            else:
                for disease_code in disease_codes:
                    disease_instance = DiseaseCode.objects.get(disease_code=disease_code)
                    SurveyDisease.objects.create(
                        survey_id=survey,
                        disease_code=disease_instance
                    )                            
            return redirect('/profiles/')
            # context = {'form': form, "profile_edit": profile_edit}
            # return render(request, 'profiles/profile_info.html', context)
    else:
        form = ProfileInfo(initial={
            'name': profile_edit.profile_name,
            'birth': profile_edit.profile_birth,
            'sex': profile_edit.survey.survey_sex,
            'pregnancy': profile_edit.survey.survey_pregnancy_code,
            'height': profile_edit.survey.survey_height,
            'weight': profile_edit.survey.survey_weight,
            'smoke': profile_edit.survey.survey_smoke,
            'alcohol': profile_edit.survey.survey_alcohol_code,
            'allergy': [allergy.allergy_code for allergy in profile_edit.surveyallergy_set.all()],
            'disease': [disease.disease_code for disease in profile_edit.surveydisease_set.all()]
        })
    # else:
    #     form = ProfileInfo(instance=profile_edit)
    print(f'반환: {profile_edit.profile_name}')
    context = {'form': form, "profile_edit": profile_edit}
    return render(request, 'profiles/profile_info.html', context)