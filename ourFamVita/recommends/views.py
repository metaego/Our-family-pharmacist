from django.shortcuts import render
from ourFamVita.models import Profile, Survey, SurveyAllergy, SurveyDisease, DiseaseCode, AllergyCode
from datetime import datetime


# Create your views here.
def recom_info(request):
    # ai 추천받기: 나의 프로필 정보 확인
    # ai 영양제 추천받기 전 나의 프로필 정보 확인 페이지
    # /recommends/{profile-id}/info
    profile = Profile.objects.get(profile_id=1)
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


    # 성별
    if survey.survey_sex == 'f' :
        survey.survey_sex = '여성'
    else:
        survey.survey_sex = '남성'


    # 임신상태
    if survey.survey_pregnancy_code == 'P0' :
        survey.survey_pregnancy_code = '해당 사항 없음'
    elif survey.survey_pregnancy_code == 'P1' :
        survey.survey_pregnancy_code = '임신 계획 중'
    elif survey.survey_pregnancy_code == 'P2' :
        survey.survey_pregnancy_code = '수유 중'
    elif survey.survey_pregnancy_code == 'P3' :
        survey.survey_pregnancy_code = '임신 중'


    # 알레르기 여부
    ## 알레르기를 기입한 적이 없는 경우
    profile_allergy = SurveyAllergy.objects.filter(survey_id=survey.survey_id).get()
    allergy_code = AllergyCode.objects.get(allergy_code=profile_allergy.allergy_code.allergy_code)


    # 키
    
#     CREATE TABLE IF NOT EXISTS `ourFamVitaDB`.`survey_allergy` (
#   `survey_allergy_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `survey_id` BIGINT UNSIGNED NOT NULL,
#   `allergy_code` VARCHAR(20) NOT NULL,
#   INDEX `allergy_code` (`allergy_code` ASC) VISIBLE,
#   PRIMARY KEY (`survey_allergy_id`),
#   UNIQUE INDEX `survey_allergy_id_UNIQUE` (`survey_allergy_id` ASC) VISIBLE,
#   CONSTRAINT `fk_sval_allergy_code`
#     FOREIGN KEY (`allergy_code`)
#     REFERENCES `ourFamVitaDB`.`allergy_info` (`allergy_code`)
#     ON DELETE CASCADE,
#   CONSTRAINT `fk_sval_survey_id`
#     FOREIGN KEY (`survey_id`)
#     REFERENCES `ourFamVitaDB`.`survey` (`survey_id`)
#     ON DELETE CASCADE)


    # 몸무게


    # 기저질환
    profile_disease = SurveyDisease.objects.filter(survey=survey.survey_id).get()
    disease_code = DiseaseCode.objects.get(disease_code=profile_disease.disease_code.disease_code)


    # 음주여부
    


    return render(request, 'recommends/recom_profile_info.html', {
        'profile': profile,
        'age': age,
        'survey': survey,
        'allergy': allergy_code.allergy_code_name,
        'disease': disease_code.disease_code_name,
    })

    

def recom_profile_total_report(request):
    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기> 영양 성분 리포트
    # /recommends/{profile-id}/surveys/{survey-id}
    return render(request, 'recommends/recom_profile_report.html')


def recom_products_nutri_base(request):
    # AI추천받기: 영양제 추천 목록(영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-nut-products/{nutri-num}
    return render(request, 'recommends/recom_profile_product_list.html')


def recom_products_profile_base(request):
    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 리포트 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-total-products/
    return render(request, 'recommends/recom_profile_product_list.html')


def recom_products_collabo_base(request):
    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(나이 & 성별 기반)
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    # /recommends/{profile-id}/surveys/{survey-id}/rec-products/
    return render(request, 'recommends/recom_profile_product_list.html')