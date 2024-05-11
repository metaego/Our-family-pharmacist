from django.shortcuts import render
from users.models import Profile, Survey, ComCode, SurveyAllergy, AllergyCode
# Create your views here.
def home_main(request, profile_id):
    # profile 데이터 가져오기
    profile = Profile.objects.get(profile_id=profile_id)
    
    
    # profile의 최신 설문조사 데이터 가져오기
    survey = Survey.objects.filter(profile_id=profile_id).latest('created_at')

    # 임신상태
    pregnancy = ComCode.objects.get(com_code=survey.survey_pregnancy_code)
    
    
    # 연령대, 성별, 임신상태, 알레르기 여부



    # 알레르기 여부
    profile_allergys = SurveyAllergy.objects.filter(survey_id=survey.survey_id).all()
    profile_allergys = profile_allergys.values_list('allergy_code', flat=True)
    print(list(profile_allergys))
    # allergy_code = AllergyCode.objects.get(allergy_code=profile_allergy.allergy_code.allergy_code)
    # print(profile_allergy.allergy_code)

    return render(request, 'home/main.html', {
        'profile': profile,
        'profile_id':profile_id,
        'survey': survey,
        'pregnancy': pregnancy.com_code_name,
        # 'allergy': allergy_code.allergy_code_name
    })