from django.shortcuts import render
from datetime import datetime
from users.models import (Profile, Survey, SurveyAllergy, SurveyDisease, DiseaseCode
                               , AllergyCode, ComCode, Product) # 코드 가독성을 위해 () 사용
from .cal_weight_and_height import impute_weight, impute_height 


# Create your views here.

def recom_info(request, profile_id):
    # ai 추천받기: 나의 프로필 정보 확인
    # ai 영양제 추천받기 전 나의 프로필 정보 확인 페이지
    # /recommends/{profile-id}/info
    profile = Profile.objects.get(profile_id=profile_id)
    survey = Survey.objects.filter(profile_id=profile.profile_id).get()
    
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


    # 임신상태
    profile_pregnancy = ComCode.objects.get(com_code=survey.survey_pregnancy_code)
    

    # 알레르기 여부
    ## 알레르기를 기입한 적이 없는 경우
    profile_allergy = SurveyAllergy.objects.filter(survey_id=survey.survey_id).get()
    allergy_code = AllergyCode.objects.get(allergy_code=profile_allergy.allergy_code.allergy_code)


    # 키
    if survey.survey_height == None:
        survey.survey_height = impute_height(survey.survey_sex, age)


    # 몸무게
    if survey.survey_weight == None:
        survey.survey_weight = impute_weight(survey.survey_sex, age)


    # 성별
    if survey.survey_sex == 'f':
        survey.survey_sex = '여성'
    else:
        survey.survey_sex = '남성'


    # 기저질환
    profile_disease = SurveyDisease.objects.filter(survey=survey.survey_id).get()
    disease_code = DiseaseCode.objects.get(disease_code=profile_disease.disease_code.disease_code)


    # 음주여부
    profile_alcohol = ComCode.objects.filter(com_code=survey.survey_alcohol_code).get()
    
    
    return render(request, 'recommends/recom_profile_info.html', {
        'profile': profile,
        'profile_id': profile_id,
        'age': age,
        'survey': survey,
        'survey_id': survey.survey_id,
        'allergy': allergy_code.allergy_code_name,
        'disease': disease_code.disease_code_name,
        'alcohol': profile_alcohol.com_code_name,
        'pregnancy': profile_pregnancy.com_code_name,
    })

    

def recom_profile_total_report(request, profile_id, survey_id):
    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기> 영양 성분 리포트
    # /recommends/{profile-id}/surveys/{survey-id}
    # profile = Profile.objects.get(profile_id=profile_id)
    # survey = Survey.objects.filter(survey_id=survey_id).get()

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


def recom_products_collabo_base(request):
    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(나이 & 성별 기반)
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    # /recommends/{profile-id}/surveys/{survey-id}/rec-products/
    return render(request, 'recommends/recom_profile_product_list.html')