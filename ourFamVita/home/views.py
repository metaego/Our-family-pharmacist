from django.shortcuts import render
from users.models import (Profile, Survey, ComCode, SurveyAllergy, 
                          AllergyCode, Recommendation, RecommendationProduct)
# Create your views here.
def home_main(request, profile_id):
    # profile 데이터 가져오기
    profile = Profile.objects.get(profile_id=profile_id)
    
    

    # profile의 최신 설문조사 데이터 가져오기
    survey = Survey.objects.filter(profile_id=profile_id).latest('created_at')



    # 임신상태
    pregnancy = ComCode.objects.get(com_code=survey.survey_pregnancy_code)
    
    
    
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
    print(kr_allergy_codes)



    # survey 기반 추천받은 영양제
    recommendation = Recommendation.objects.filter(survey_id=survey.survey_id)
    if recommendation.exists():
        # 영양제 리스트 추출
        print('실행!')
        pass
    recommendation = None
    print('recommendation: ', recommendation, type(recommendation))
    
    # 추천 받았는지 여부 확인
    # 영양제 번호, 이미지 주소


    return render(request, 'home/main.html', {
        'profile': profile,
        'profile_id':profile_id,
        'survey': survey,
        'pregnancy': pregnancy.com_code_name,
        'allergys': kr_allergy_codes,
        'recommendation': recommendation,
    })