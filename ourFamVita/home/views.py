import os
import requests, json
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from users.models import (Profile, Product
                          , Survey, SurveyAllergy
                          , ComCode, AllergyCode 
                          , Recommendation, RecommendationProduct
                          )
from dotenv import load_dotenv
import time
# Create your views here.
def home_main(request, profile_id):
    start_time = time.time()
    
    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    # profile 데이터 가져오기
    profile = Profile.objects.get(profile_id=profile_id)
    
    

    # profile의 최신 설문조사 데이터 가져오기
    survey = Survey.objects.filter(profile_id=profile_id).latest('created_at')



    # 임신상태
    pregnancy = ComCode.objects.get(com_code=survey.survey_pregnancy_code)
    
    
    
    # 알레르기 : 전체 알레르기 보여주는 것이 아닌 여부만 노출
    ## profile allergy 가져오기
    profile_allergys = SurveyAllergy.objects.filter(survey_id=survey.survey_id).values_list('allergy_code', flat=True)
    profile_allergys = list(profile_allergys)
    ## profile allergy 코드를 한글 코드명으로 변환
    kr_allergy_codes = []
    for profile_allergy_code in profile_allergys:
        kr_allergy_code = AllergyCode.objects.filter(allergy_code=profile_allergy_code).values_list('allergy_code_name')
        kr_allergy_code = ''.join(kr_allergy_code[0])
        kr_allergy_codes.append(kr_allergy_code)
    # print(kr_allergy_codes)



    # survey 기반 추천받은 영양제
    print(f'survey.survey_id: {survey.survey_id}')
    recommendation = Recommendation.objects.filter(survey_id=survey.survey_id).exists()
    print(f'home main recommendation: {recommendation}')
    survey_base_recom_products = None
    if recommendation:
        # 영양제 리스트 추출
        recommendation = Recommendation.objects.get(survey_id=survey.survey_id)
        recommendation_products = RecommendationProduct.objects.filter(recommendation_id=recommendation.recommendation_id).values_list('product_id', flat=True)
        recommendation_products = list(recommendation_products)
        survey_base_recom_products = Product.objects.filter(product_id__in=recommendation_products)
        survey_base_recom_products = survey_base_recom_products[:3]
        

    # 연령*성별 기반 추천받은 영양제
    # flask 요청 
    client_ip = request.META.get('REMOTE_ADDR', None)
    print(f'client_ip: {client_ip}')
    # content = {
    #     'profile_id': profile_id,
    #     'survey_id': survey_id
    # }
    if client_ip == '127.0.0.1':
        pass
    elif client_ip != os.environ.get('AWS_PUBLIC_IP'):
         client_ip = os.environ.get('AWS_PUBLIC_IP')
    csrf_token = get_token(request)
    response = requests.post('http://' + client_ip + f':5000/ai-collabo-recom/{survey.survey_id}', 
                            #  data=json.dumps(content), 
                                headers={'X-CSRFToken': csrf_token,
                                        'Content-Type': 'application/json'})
    
    contents = json.loads(response.text)
    print(f'contents(home): {contents}')
    recom_product_sex_age_list = contents['recom_product_sex_age_list']
    sex_age_base_recom_products = Product.objects.filter(product_id__in=recom_product_sex_age_list)
    
    
    # 실행 시간 계산
    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)

    print("Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")
    
    return render(request, 'home/main.html', {
        'profile': profile,
        'profile_id':profile_id,
        'survey': survey,
        'pregnancy': pregnancy.com_code_name,
        'allergys': kr_allergy_codes,
        'recommendation': recommendation,
        'survey_base_recom_products': survey_base_recom_products,
        'sex_age_base_recom_products': sex_age_base_recom_products[:3],
    })