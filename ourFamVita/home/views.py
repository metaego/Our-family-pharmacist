from django.shortcuts import render
from users.models import Profile, Survey
# Create your views here.
def home_main(request, profile_id, survey_id):
    # profile 데이터 가져오기
    profile = Profile.objects.get(profile_id=1)
    profile_id = profile.profile_id
    
    # profile의 최신 설문조사 데이터 가져오기
    survey = Survey.objects.filter(profile_id=profile_id).order_by('-created_at').first()
    if survey.survey_sex == 'f' :
        survey.survey_sex = '여성'
    else:
        survey.survey_sex = '남성'
    print(profile_id)
    return render(request, 'home/main.html', {
        'profile': profile,
        'profile_id':profile_id,
        'survey': survey
    })