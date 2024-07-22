from django.shortcuts import render, redirect
from datetime import datetime
from users.models import (Profile
                        , Survey #,  SurveyAllergy, SurveyDisease, SurveyFunction  
                        , ComCode #, DiseaseCode, AllergyCode, FunctionCode
                        # , RecommendationIngredient, RecommendationProduct, Recommendation
                        # , Product, Ingredient, ProductIngredient # 코드 가독성을 위해 () 사용
                        )
from django.db.models import Count
# from .cal_weight_and_height import impute_weight, impute_height 
from django.utils import timezone
from urllib.parse import unquote
import requests
# from django.http import HttpResponse
from django.middleware.csrf import get_token
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Create your views here.

def recom_info(request):
    start_time = time.time()
    # ai 추천받기: 나의 프로필 정보 확인
    # ai 영양제 추천받기 전 나의 프로필 정보 확인 페이지
    # /recommends/{profile-id}/info

    user_id = request.session.get('_auth_user_id')
    profile_id = request.session.get('profile_id')
    if not user_id:
        return redirect('/')

    # 프로필 및 survey 데이터 가져오기
    profile = Profile.objects.get(pk=profile_id)
    survey = Survey.objects.filter(profile_id=profile.pk).latest('survey_created_at')
    # print("survey_id(recom_info): ", survey.survey_id)


    
    # 만나이 계산
    survey_birth = str(profile.profile_birth)
    birth = datetime.strptime(survey_birth, '%Y-%m-%d').date()
    today = datetime.now().date()
    age = today.year - int(survey_birth[:4])
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
    pregnancy_code = survey.survey_pregnancy_code
    pregnancy_kr_code = ComCode.objects.filter(com_code=pregnancy_code).values_list('com_code_name', flat=True)
    pregnancy_kr_code = ''.join(list(pregnancy_kr_code))



    # 알레르기 여부
    allergy_code_dict = survey.survey_allergy_code
    allergy_kr_list = []
    if type(allergy_code_dict['ALLERGY']) == str:
        code = ComCode.objects.filter(com_code=allergy_code_dict['ALLERGY']).values_list('com_code_name', flat=True)
        code = ''.join(list(code))
        allergy_kr_list.append(allergy_kr_list)

    else: 
        for code_list in allergy_code_dict.values():
            for code in code_list:
                code = ComCode.objects.filter(com_code=code).values_list('com_code_name', flat=True)
                code = ''.join(list(code))
                if code != 'DI00':
                    allergy_kr_list.append(code)
    print(f'allergy_kr_list: {allergy_kr_list}')


    # for code_list in allergy_code_dict.values():
    #     for code in code_list:
    #         code = ComCode.objects.filter(com_code=code).values_list('com_code_name', flat=True)
    #         code = ', '.join(list(code))
    #         allergy_kr_list.append(code)
    # allergy_kr_list = ', '.join(allergy_kr_list)
    # print(f'allergy_kr_list: {allergy_kr_list}')



    # 키
    if survey.survey_height == None:
        survey.survey_height = '미입력'


    # 몸무게
    if survey.survey_weight == None:
        survey.survey_weight = '미입력'



    # 기저질환
    disease_code_dict = survey.survey_disease_code
    disease_kr_list = []
    print(f'disease_code_dict: {disease_code_dict}')
    # survey 테이블 survey_disease_code 컬럼의 'DISEASE' 키 값이 1개일 때 리스트로 바뀐다면 아래 코드 수정해야 함 
    if type(disease_code_dict['DISEASE']) == str:
        code = ComCode.objects.filter(com_code=disease_code_dict['DISEASE']).values_list('com_code_name', flat=True)
        code = ''.join(list(code))
        disease_kr_list.append(code)

    else: 
        for code_list in disease_code_dict.values():
            for code in code_list:
                code = ComCode.objects.filter(com_code=code).values_list('com_code_name', flat=True)
                code = ''.join(list(code))
                disease_kr_list.append(code)
    print(f'disease_kr_list: {disease_kr_list}')




    # 음주여부
    alcohol_code = survey.survey_alcohol_code
    alcohol_code = ComCode.objects.filter(com_code=alcohol_code).values_list('com_code_name', flat=True)
    alcohol_code = ''.join(list(alcohol_code))
    print(f'alcohol_code: {alcohol_code}')
    
    

    # 흡연여부
    smoking_code = survey.survey_smoking_code
    smoking_code = ComCode.objects.filter(com_code=smoking_code).values_list('com_code_name', flat=True)
    smoking_code = ''.join(list(smoking_code))
    print(f'smoking_code: {smoking_code}')



    # 건강고민 순위 리스트
    function_list = ComCode.objects.filter(com_code_grp='FUNCTION').exclude(com_code='HF00').values_list('com_code', flat=True)
    function_list = list(function_list)
    i = 0
    for code in function_list:
        code = ComCode.objects.filter(com_code=code).values_list('com_code_name', flat=True)
        code = ''.join(list(code))
        function_list[i] = code
        i += 1
    print(f'function_list: {function_list}')



    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("recom_info Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return render(request, 'recommends/recom_profile_info.html', {
        'profile': profile,
        'survey': survey,
        'age': age,
        'allergy': allergy_kr_list,
        'disease': disease_kr_list,
        'alcohol': alcohol_code,
        'pregnancy': pregnancy_kr_code,
        'smoking': smoking_code,
        'function_code_list': function_list,
    })

    

def save_survey_data(request, profile_id, survey_id):
    start_time = time.time()

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')

    if request.method == 'POST':
        selected_functions = [unquote(code) for code in request.POST.getlist('checkbox[]')]

        # 새로운 survey 데이터 생성
        survey = Survey.objects.get(survey_id=survey_id)
        survey.pk = None
        survey.created_at = timezone.now()
        survey.save()

        survey = Survey.objects.get(survey_id=survey.survey_id)
        # print(f'save_survey_data(survey.survey_id): {survey.survey_id}')
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
        if not selected_functions:
            function_code = FunctionCode.objects.get(function_code='HF00')
            SurveyFunction.objects.create(survey_id=survey, function_code=function_code)
            # print('건강기능 고민을 아무것도 선택하지 않았을 때')
        else:
            for kr_f_code in selected_functions:
                function_code = FunctionCode.objects.get(function_code_name=kr_f_code)
                SurveyFunction.objects.create(survey_id=survey, function_code=function_code)
            # print('survey, survey_disease, survey_allergey, survey_function data 신규 생성...!')

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("save_survey_data function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:request_flask_recom_model', profile_id, survey.survey_id)


def request_flask_recom_model(request, profile_id, survey_id):

    start_time = time.time()

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    client_ip = request.META.get('REMOTE_ADDR', None)

    if client_ip != '127.0.0.1' and client_ip != os.environ.get('AWS_PUBLIC_IP'):
        client_ip = os.environ.get('AWS_PUBLIC_IP')
    csrf_token = get_token(request)
    survey = Survey.objects.filter(profile_id=profile_id).latest('created_at')
    # print(f'최근 survey_id: {survey.survey_id}')
    response = requests.post('http://' + client_ip + f':5000/ai-total-recom/{survey.survey_id}/', 
                                headers={'X-CSRFToken': csrf_token,
                                        'Content-Type': 'application/json'})
    
    contents = json.loads(response.text)
    request.session['contents'] = contents
    # print(f'contents(플라스크 토탈 추천): {contents}')
    # print(type(contents))
    profile = Profile.objects.get(profile_id=profile_id)

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("request_flask_recom_model function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:profile_total_report', profile.profile_id, survey.survey_id)




def recom_profile_total_report(request, profile_id, survey_id):

    start_time = time.time()

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')

    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기> 영양 성분 리포트
    # /recommends/{profile-id}/surveys/{survey-id}
    profile = Profile.objects.get(profile_id=profile_id)
    survey = Survey.objects.get(survey_id=survey_id)
    # print(profile_id)
    # print(f'profile_id(recom_profile_total_report): {profile.profile_id}')
    # print(survey_id)
    # print(f'survey_id(recom_profile_total_report): {survey.survey_id}')
   
    # 세션에서 contents 가져오기
    contents = request.session.get('contents', {})
    print(f'contents(recom_profile_total_report): {contents}')



    # 1) 추천 영양 성분 가져오기
    ## 영양 성분명, 주요건강기능, 일일 섭취량 상하한
    recommendation = Recommendation.objects.get(survey_id=survey_id)
    recommendation_ingredients = RecommendationIngredient.objects.filter(recommendation_id=recommendation.recommendation_id).values_list('ingredient_id', flat=True)
    recommendation_ingredients = list(recommendation_ingredients)
    # print(f'recommendation_ingredients: {recommendation_ingredients}') # [150, 362]
    # print()

    recommend_ingredients = Ingredient.objects.filter(ingredient_id__in=recommendation_ingredients)
    # print(recommend_ingredients) # <QuerySet [<Ingredient: Ingredient object (150)>, <Ingredient: Ingredient object (362)>]>
    # print()



    # 2) 영양 성분 리포트 바탕으로 영양제 추천
    ## recommendation_product에서 데이터 가져오기
    recommendation_products = RecommendationProduct.objects.filter(recommendation_id=recommendation.recommendation_id).values_list('product_id', flat=True)
    recommendation_products = list(recommendation_products)
    # print(f'recommendation_products: {recommendation_products}') # [200400150831149, 200400200072802]
    # print()

    recommend_products = Product.objects.filter(product_id__in=recommendation_products)
    # print(f'products: {recommend_products}') # <QuerySet [<Product: Product object (200400150831149)>, <Product: Product object (200400200072802)>]>
    # print()

    
    
    # 3) 성별*연령 기반 영양제 추천
    ## 성별*연령별 기반 영양제
    collabo_recomm_product_list = contents['recom_product_sex_age_list']
    collabo_recommendation_products = Product.objects.filter(product_id__in=collabo_recomm_product_list)

    
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


    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("recom_profile_total_report function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return render(request, 'recommends/recom_profile_report.html', {
        'profile': profile,
        'survey':survey,
        'recommend_ingredients': recommend_ingredients,
        'recommend_products': recommend_products[:3], # 영양 성분 리포트 바탕 추천 product
        'collabo_recommendation_products' : collabo_recommendation_products[:3], # 연령*성별 기반 추천
        'age': age,
        'allergy': kr_allergy_codes,
        'disease': kr_disease_codes,
        'alcohol': profile_alcohol.com_code_name,
        'pregnancy': profile_pregnancy.com_code_name,
    })



def recom_products_nutri_base(request, profile_id, survey_id, nutri_num):
    
    start_time = time.time()

    # AI추천받기: 영양제 추천 목록(영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-nut-products/{nutri-num}
    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    # 프로필 및 survey 데이터 가져오기
    profile = Profile.objects.get(profile_id=profile_id)
    survey = Survey.objects.get(survey_id=survey_id)


    
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


    # 추천받은 영양 성분 정보
    recommend_ingredient = Ingredient.objects.get(ingredient_id=nutri_num)


    # 추천받은 영양 성분을 가진 제품 리스트
    nutrient_included_products = ProductIngredient.objects.filter(ingredient_id=nutri_num).values_list('product_id', flat=True)
    nutrient_included_products = list(nutrient_included_products)
    popular_products = Product.objects.filter(product_id__in=nutrient_included_products).order_by('-product_rating_avg', '-product_rating_cnt')[:20]
    
    

    page_flag = '추천 영양 성분 기반'

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("recom_products_nutri_base function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return render(request, 'recommends/recom_profile_product_list.html', {
        'profile': profile,
        'survey': survey,
        'age': age,
        'allergy': kr_allergy_codes,
        'disease': kr_disease_codes,
        'alcohol': profile_alcohol.com_code_name,
        'pregnancy': profile_pregnancy.com_code_name,
        'recommend_ingredient': recommend_ingredient,
        'popular_products': popular_products,
        'page_flag': page_flag,
        'nutri_num': nutri_num,
    })



def recom_products_profile_base(request, profile_id, survey_id):

    start_time = time.time()
    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 리포트 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-total-products/
    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')

    profile = Profile.objects.get(profile_id=profile_id)
    survey = Survey.objects.get(survey_id=survey_id)
    # print(f'profile_id(recom_products_profile_base): {profile_id}')
    # print(f'survey_id(recom_products_profile_base): {survey_id}')

    # ai 추천 받은 후 추천해주는 제품의 product_id가 필요
    recommendation = Recommendation.objects.get(survey_id=survey_id)
    recom_product_list = RecommendationProduct.objects.filter(recommendation_id=recommendation.recommendation_id).values_list('product_id', flat=True)
    recom_product_list = list(recom_product_list)

    popular_products = Product.objects.filter(product_id__in=recom_product_list)
    print(f'popular_products(영양성분리포트기반): {popular_products}')

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



    # 추천 영양제 리스트
    page_flag = '영양 성분 리포트'

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("recom_products_profile_base function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return render(request, 'recommends/recom_profile_product_list.html', {
        'profile': profile,
        'survey': survey,
        'age': age,
        'allergy': kr_allergy_codes,
        'disease': kr_disease_codes,
        'alcohol': profile_alcohol.com_code_name,
        'pregnancy': profile_pregnancy.com_code_name,
        'popular_products': popular_products,
        'page_flag': page_flag,
    })



def request_flask_collabo_recom_model(request, profile_id):

    start_time = time.time()

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    profile = Profile.objects.get(profile_id=profile_id)
    survey = Survey.objects.filter(profile_id=profile.pk).latest('created_at')
    
    # flask 요청 
    client_ip = request.META.get('REMOTE_ADDR', None)

    if client_ip != '127.0.0.1' and client_ip != os.environ.get('AWS_PUBLIC_IP'):
        client_ip = os.environ.get('AWS_PUBLIC_IP')
    
    csrf_token = get_token(request)
    response = requests.post('http://' + client_ip + f':5000/ai-collabo-recom/{survey.survey_id}', 
                            #  data=json.dumps(content), 
                                headers={'X-CSRFToken': csrf_token,
                                        'Content-Type': 'application/json'})
    
    contents = json.loads(response.text)
    print(f'flask에서 응답 받은 내용 출력: {contents}')
    print(type(contents))

    request.session['contents'] = contents
    
    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("request_flask_collabo_recom_model function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:products_collabo_base', profile.profile_id)



def recom_products_collabo_base(request, profile_id):
    
    start_time = time.time()

    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(나이 & 성별 기반)
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    # /recommends/{profile-id}/rec-products/

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')

    # 세션에서 contents 가져오기
    contents = request.session.get('contents', {})
    # print(f'contents: {contents}')
    profile = Profile.objects.get(profile_id=profile_id)
    survey = Survey.objects.get(survey_id=contents['survey_id'])

    # ai 추천 받은 후 추천해주는 제품의 product_id가 필요
    collabo_product_list = contents['recom_product_sex_age_list']
    popular_products = Product.objects.filter(product_id__in=collabo_product_list)

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



    page_flag = '연령 및 성별 기반'

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("recom_products_collabo_base function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return render(request, 'recommends/recom_profile_product_list.html', {
        'profile': profile,
        'survey': survey,
        'age': age,
        'allergy': kr_allergy_codes,
        'disease': kr_disease_codes,
        'alcohol': profile_alcohol.com_code_name,
        'pregnancy': profile_pregnancy.com_code_name,
        'popular_products': popular_products,
        'page_flag': page_flag,
    })



def request_flask_recom_model_old(request, profile_id, survey_id):
    start_time = time.time()

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    profile = Profile.objects.get(profile_id=profile_id)
    survey = Survey.objects.filter(survey_id=survey_id)
    
    # flask 요청 
    client_ip = request.META.get('REMOTE_ADDR', None)

    if client_ip != '127.0.0.1' and client_ip != os.environ.get('AWS_PUBLIC_IP'):
        client_ip = os.environ.get('AWS_PUBLIC_IP')
    
    csrf_token = get_token(request)
    response = requests.post('http://' + client_ip + f':5000/ai-total-recom-old/{survey_id}', 
                                headers={'X-CSRFToken': csrf_token,
                                        'Content-Type': 'application/json'})
    
    contents = json.loads(response.text)
    print(f'flask에서 응답 받은 내용 출력: {contents}')
    print(type(contents))

    request.session['contents'] = contents
    
    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("request_flask_collabo_recom_model function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:profile_total_report', profile.profile_id, survey_id)