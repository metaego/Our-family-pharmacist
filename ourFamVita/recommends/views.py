from django.shortcuts import render
from datetime import datetime
from users.models import (Profile, Survey, SurveyAllergy, SurveyDisease, DiseaseCode
                        , AllergyCode, ComCode, Product, SurveyFunction
                        , FunctionCode) # 코드 가독성을 위해 () 사용
from django.db.models import Count, Q
# from .cal_weight_and_height import impute_weight, impute_height 
from django.http import HttpResponse
from django.utils import timezone
from urllib.parse import unquote


# Create your views here.

def recom_info(request, profile_id):
    # ai 추천받기: 나의 프로필 정보 확인
    # ai 영양제 추천받기 전 나의 프로필 정보 확인 페이지
    # /recommends/{profile-id}/info

    # 프로필 및 survey 데이터 가져오기
    profile = Profile.objects.get(pk=profile_id)
    survey = Survey.objects.filter(profile_id=profile.pk).latest('-created_at')
    # print("survey_id: ", survey.survey_id)


    
    # 만나이 계산
    profile_birth = str(profile.profile_birth)
    birth = datetime.strptime(profile_birth, '%Y-%m-%d').date()
    today = datetime.now().date()
    age = today.year - int(profile_birth[:4])
    ## 생일이 있는 달을 아직 안 지남
    if today.month < birth.month:
        age -= 1

    ## 현재 월이 생일이 있는 달이지만 생일 일자가 아직 안 지남
    elif today.month == birth.month and today.day < birth.day:
        age -= 1



    # 성별
    if survey.survey_sex == 'f':
        survey.survey_sex = '여성'
    else:
        survey.survey_sex = '남성'



    # 임신상태
    profile_pregnancy = ComCode.objects.get(com_code=survey.survey_pregnancy_code)
    


    # 알레르기 여부
    ## profile allergy 가져오기
    profile_allergys = SurveyAllergy.objects.filter(survey_id=survey.survey_id).values_list('allergy_code', flat=True)
    profile_allergys = list(profile_allergys)
    ## profile allergy 코드를 한글 코드명으로 변환
    kr_allergy_codes = []
    for profile_allergy_code in profile_allergys:
        kr_allergy_code = AllergyCode.objects.filter(allergy_code=profile_allergy_code).values_list('allergy_code_name')
        kr_allergy_code = ''.join(kr_allergy_code[0])
        kr_allergy_codes.append(kr_allergy_code)



    # 키
    if survey.survey_height == None:
        survey.survey_height = '미입력'


    # 몸무게
    if survey.survey_weight == None:
        survey.survey_weight = '미입력'



    # 기저질환
    profile_disease = SurveyDisease.objects.filter(survey_id=survey.survey_id).values_list('disease_code', flat=True)
    profile_disease = list(profile_disease)
    # print(f'profile_disease: {profile_disease}') #  ['DI01', 'DI02', 'DI03', 'DI04', 'DI07']
    kr_disease_codes = []
    for profile_disease_code in profile_disease:
        kr_disease_code = DiseaseCode.objects.filter(disease_code=profile_disease_code).values_list('disease_code_name', flat=True)
        kr_disease_code = str(kr_disease_code[0])
        kr_allergy_code = ''.join(kr_disease_code)
        kr_disease_codes.append(kr_disease_code)
    # print(f'kr_disease_codes_list: {kr_disease_codes}')



    # 음주여부
    profile_alcohol = ComCode.objects.filter(com_code=survey.survey_alcohol_code).get()
    
    

    # 흡연여부
    if survey.survey_smoke == 'y':
        survey.survey_smoke = '흡연'
    else:
        survey.survey_smoke = '비흡연'


    # 건강고민 순위 리스트
    ## 사용자들 설문조사에서 건강고민 순위 매기기
    survey_function_codes = SurveyFunction.objects.exclude(function_code='HF00')
    survey_function_codes = survey_function_codes.values('function_code').annotate(count=Count('function_code'))
    survey_function_codes = survey_function_codes.order_by('-count')
    survey_function_codes = list(survey_function_codes)
    ## 건강고민 코드만 가져오기
    function_code_list = []
    for items in survey_function_codes:
        function_code_list.append(items['function_code'])
    ## 누락된 건강코드 추가
    all_function_code = FunctionCode.objects.exclude(function_code='HF00').values_list('function_code', flat=True)
    all_function_code = list(all_function_code)
    for code in all_function_code:
        if code not in function_code_list:
            function_code_list.append(code)
    ## 코드명을 한글명으로 변환
    kr_function_code_list = []
    for code in function_code_list:
        kr_code = FunctionCode.objects.filter(function_code=code).values_list('function_code_name', flat=True)
        kr_code = ''.join(kr_code)
        kr_function_code_list.append(kr_code)
    # print(f'kr_function_code_list: {kr_function_code_list}')



    return render(request, 'recommends/recom_profile_info.html', {
        'profile': profile,
        'survey': survey,
        'age': age,
        'allergy': kr_allergy_codes,
        'disease': kr_disease_codes,
        'alcohol': profile_alcohol.com_code_name,
        'pregnancy': profile_pregnancy.com_code_name,
        'function_code_list': kr_function_code_list,
    })

    

def request_flask_recom_model(request, profile_id, survey_id):
    # post로 요청이 들어오면 건강고민 설문을 DB에 저장
    # flask 추천 알고리즘 request
    if request.method == 'POST':
        selected_functions = [unquote(code) for code in request.POST.getlist('checkbox[]')]

        # 새로운 survey 데이터 생성
        survey = Survey.objects.get(survey_id=survey_id)
        survey.pk = None
        survey.created_at = timezone.now()
        survey.save()

        survey = Survey.objects.get(survey_id=survey.survey_id)

        # 새로운 survey_disease 데이터 생성
        survey_diseases = SurveyDisease.objects.filter(survey_id=survey_id).values_list('disease_code', flat=True)
        survey_diseases = list(survey_diseases)  # ['DI01', 'DI02', 'DI03', 'DI04', 'DI05']
        for d_code in survey_diseases:
            disease_code = DiseaseCode.objects.get(disease_code=d_code)
            SurveyDisease.objects.create(survey_id=survey, disease_code=disease_code)
           


        # 새로운 survey_allergy 데이터 생성
        survey_allerges = SurveyAllergy.objects.filter(survey_id=survey_id).values_list('allergy_code', flat=True)
        survey_allerges = list(survey_allerges)
        for a_code in survey_allerges:
            allergy_code = AllergyCode.objects.get(allergy_code=a_code)
            SurveyAllergy.objects.create(survey_id=survey, allergy_code=allergy_code)



        # 새로운 survey_function 데이터 생성
        for kr_f_code in selected_functions:
            function_code = FunctionCode.objects.get(function_code_name=kr_f_code)
            SurveyFunction.objects.create(survey_id=survey, function_code=function_code)
        print('survey, survey_disease, survey_allergey, survey_function data 신규 생성...!')
        return HttpResponse('return!')



def recom_profile_total_report(request, profile_id, survey_id):
    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기> 영양 성분 리포트
    # /recommends/{profile-id}/surveys/{survey-id}
    # profile = Profile.objects.get(profile_id=profile_id)
    # survey = Survey.objects.filter(survey_id=survey_id).get()




    # flask에서 전달 받은 내용을 장고 html에 보여주기

    print("profile_id: ", profile_id, survey_id)
    return render(request, 'recommends/recom_profile_report.html', {
        'profile_id': profile_id,
        'survey_id':survey_id,
    })


def recom_products_nutri_base(request):
    # AI추천받기: 영양제 추천 목록(영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-nut-products/{nutri-num}
    return render(request, 'recommends/recom_profile_product_list.html')


def recom_products_profile_base(request, profile_id, survey_id):
    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 리포트 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-total-products/
    profile = Profile.objects.get(profile_id=profile_id)
    # survey = Survey.objects.filter(survey_id=survey_id).get()

    # ai 추천 받은 후 추천해주는 제품의 product_id가 필요
    product_id = 1
    product = Product.objects.get(product_id=product_id)
    return render(request, 'recommends/recom_profile_product_list.html', {
        'profile': profile,
        'survey_id': survey_id,
        'product': product,
    })


def recom_products_collabo_base(request, profile_id):
    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(나이 & 성별 기반)
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    # /recommends/{profile-id}/rec-products/
    # 해당 함수는 flask 서버와 연결 필요
    profile = Profile.objects.get(pk=profile_id)

    # 추천받은 product가 없어서 임의로 넣음
    # 협업필터링 ML 후 업뎃 예정 
    product = Product.objects.get(pk=1)
    return render(request, 'recommends/recom_profile_product_list.html', {
        'product': product,
        'profile': profile
    })