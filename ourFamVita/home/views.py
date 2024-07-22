import os
import requests, json
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from users.models import (Profile, Product, Survey 
                          , ComCode  
                          , Recom, RecomSurveyProduct
                          )
from dotenv import load_dotenv
import time
# Create your views here.
def home_main(request, profile_id):
    start_time = time.time()
    
    user_id = request.session.get('_auth_user_id') # dict_keys(['_auth_user_id', '_auth_user_backend', '_auth_user_hash', 'profile_id', 'survey_id'])
    # print(f'user_id: {user_id}')
    # print(f'profile_id: {profile_id}')
    
    if not user_id :
        return redirect('/')
    
    request.session['profile_id'] = profile_id


    # profile 데이터 가져오기
    profile = Profile.objects.get(profile_id=profile_id)
        


    # profile의 최신 설문조사 데이터 가져오기
    survey = Survey.objects.filter(profile_id=profile_id).latest('survey_created_at')



    # 임신상태
    pregnancy_code = survey.survey_pregnancy_code
    # print(f'pregnancy: {pregnancy_code}') # P0
    pregnancy_kr = ComCode.objects.filter(com_code=pregnancy_code).values_list('com_code_name', flat=True)
    pregnancy_kr = ''.join(list(pregnancy_kr)) # 쿼리셋을 문자열로 변경
    # print(f"pregnancy_kr: {pregnancy_kr}")


       
    # 알레르기 : 전체 알레르기 보여주는 것이 아닌 여부만 노출
    # profile allergy 가져오기
    allergy = survey.survey_allergy_code
    # print(f'allergy: {allergy}')  # {'ALLERGY': ['AL00', 'AL01', 'AL02', 'AL03', 'AL04']}
    allergy_kr_list = []
    for code_list in allergy.values():
        for code in code_list:
            # alg_code: AL00
            # 알러지 한글명으로 변환
            code = ComCode.objects.filter(com_code=code).values_list('com_code_name', flat=True)
            code = ', '.join(list(code))
            allergy_kr_list.append(code)
    # print(f'allergy_kr_list: {allergy_kr_list}') # ['해당 사항 없음', '게 또는 새우 등의 갑각류', '옻', '땅콩', '프로폴리스']
    allergy_kr = ', '.join(allergy_kr_list) # 해당 사항 없음, 게 또는 새우 등의 갑각류, 옻, 땅콩, 프로폴리스
    # print(f'allergy_kr: {allergy_kr}')



    # survey 기반 추천받은 영양제
    recom_id = Recom.objects.filter(survey_id=survey.survey_id).exists()
    survey_base_recom_products = None
    if recom_id:
        recom_product_ids = RecomSurveyProduct.objects.filter(recom_id=recom_id).values_list('product_id', flat=True)
        recom_product_ids = list(recom_product_ids)
        survey_base_recom_products = Product.objects.filter(product_id__in=recom_product_ids)
        survey_base_recom_products = survey_base_recom_products[:3]
    # print(f'survey_base_recom_products: {survey_base_recom_products}')

        

    # # 연령*성별 기반 추천받은 영양제
    # # flask 요청 
    # client_ip = request.META.get('REMOTE_ADDR', None)
    # print(f'client_ip: {client_ip}')
    # # content = {
    # #     'profile_id': profile_id,
    # #     'survey_id': survey_id
    # # }
    # if client_ip != '127.0.0.1' and client_ip != os.environ.get('AWS_PUBLIC_IP'):
    #     client_ip = os.environ.get('AWS_PUBLIC_IP')
    # csrf_token = get_token(request)
    # response = requests.post('http://' + client_ip + f':5000/ai-collabo-recom/{survey.survey_id}', 
    #                         #  data=json.dumps(content), 
    #                             headers={'X-CSRFToken': csrf_token,
    #                                     'Content-Type': 'application/json'})
    
    # contents = json.loads(response.text)
    # print(f'contents(home): {contents}')
    # recom_product_sex_age_list = contents['recom_product_sex_age_list']
    # sex_age_base_recom_products = Product.objects.filter(product_id__in=recom_product_sex_age_list)
    
    
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
        'pregnancy': pregnancy_kr,
        'allergys': allergy_kr,
        'survey_base_recom_products': survey_base_recom_products,
        # 'sex_age_base_recom_products': sex_age_base_recom_products[:3],
    })