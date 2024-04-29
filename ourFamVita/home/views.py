from django.shortcuts import render
from users.models import Profile, Survey, ComCode, SurveyAllergy, AllergyCode
# Create your views here.
def home_main(request, profile_id):
    # profile 데이터 가져오기
    profile = Profile.objects.get(profile_id=profile_id)
    
    # profile의 최신 설문조사 데이터 가져오기
    survey = Survey.objects.filter(profile_id=profile_id).order_by('-created_at').first()
    
    # 임신상태
    pregnancy = ComCode.objects.get(com_code=survey.survey_pregnancy_code)
    
    
    # 알레르기 여부
    ## 알레르기를 기입한 적이 없는 경우
    profile_allergy = SurveyAllergy.objects.filter(survey_id=survey.survey_id).get()
    allergy_code = AllergyCode.objects.get(allergy_code=profile_allergy.allergy_code.allergy_code)
    print(profile_allergy.allergy_code)

    return render(request, 'home/main.html', {
        'profile': profile,
        'profile_id':profile_id,
        'survey': survey,
        'pregnancy': pregnancy.com_code_name,
        'allergy': allergy_code.allergy_code_name
    })