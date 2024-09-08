from django.shortcuts import render, redirect
from datetime import datetime
from users.models import (Profile, Survey, ComCode 
                        , Recom, RecomIngredient, RecomSurveyProduct 
                        , Product, Ingredient, ProductIngredient 
                        ) # 코드 가독성을 위해 () 사용
from django.db.models import Count
from django.utils import timezone
from urllib.parse import unquote
import requests
from django.middleware.csrf import get_token
import json
from dotenv import load_dotenv
import os
import time
from django import forms


load_dotenv()


# Create your views here.
def recom_info(request):
    start_time = time.time()
    # ai 추천받기: 나의 프로필 정보 확인
    # ai 영양제 추천받기 전 나의 프로필 정보 확인 페이지

    user_id = request.session.get('_auth_user_id')
    profile_id = request.session.get('profile_id')
    if not user_id:
        return redirect('/')

    # 프로필 및 survey 데이터 가져오기
    profile = Profile.objects.get(pk=profile_id)
    survey = Survey.objects.filter(profile_id=profile.pk).latest('survey_created_at')

    
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


    # 키
    if survey.survey_height == None:
        survey.survey_height = '미입력'


    # 몸무게
    if survey.survey_weight == None:
        survey.survey_weight = '미입력'


    # 기저질환
    disease_code_dict = survey.survey_disease_code
    disease_kr_list = []
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


    # 음주여부
    alcohol_code = survey.survey_alcohol_code
    alcohol_code = ComCode.objects.filter(com_code=alcohol_code).values_list('com_code_name', flat=True)
    alcohol_code = ''.join(list(alcohol_code))
    
    
    # 흡연여부
    smoking_code = survey.survey_smoking_code
    smoking_code = ComCode.objects.filter(com_code=smoking_code).values_list('com_code_name', flat=True)
    smoking_code = ''.join(list(smoking_code))


    # 건강고민 순위 리스트 → survey_com_code 테이블 사용해서 건강고민 인기 순 정렬 시도해볼 것!
    function_list = ComCode.objects.filter(com_code_grp='FUNCTION').exclude(com_code='HF00').values_list('com_code', flat=True)
    function_list = list(function_list)
    i = 0
    for code in function_list:
        code = ComCode.objects.filter(com_code=code).values_list('com_code_name', flat=True)
        code = ''.join(list(code))
        function_list[i] = code
        i += 1


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

    

def save_survey_data(request, survey_id):
    start_time = time.time()
    user_id = request.session.get('_auth_user_id')

    if not user_id:
        return redirect('/')

    if request.method == 'POST':
        selected_functions = [unquote(code) for code in request.POST.getlist('checkbox[]')]

        # 새로운 survey 데이터 생성
        survey = Survey.objects.get(survey_id=survey_id)
        survey.pk = None
        survey.survey_created_at = timezone.now()

        survey_selected_functions = {}
        idx = 0
        if not selected_functions:
            survey_selected_functions =  {"1st": "HF00"}
        else:
            for kr_f_code in selected_functions:
                dict_key = ["1st", "2nd", "3rd", "4th", "5th"]
                survey_selected_functions[dict_key[idx]] = f'{kr_f_code}'
                idx += 1
        survey_selected_functions = survey_selected_functions
        print(f'survey_selected_functions: {survey_selected_functions}')       
        survey.survey_function_code = survey_selected_functions
        
        survey.save()


    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("save_survey_data function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:request_flask_total_recom')


def request_flask_total_recom(request):

    start_time = time.time()

    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('/')
    

    # flask에 요청 보내기
    client_ip = request.META.get('REMOTE_ADDR', None)
    if client_ip != '127.0.0.1' and client_ip != os.environ.get('AWS_PUBLIC_IP'):
        client_ip = os.environ.get('AWS_PUBLIC_IP')
    csrf_token = get_token(request)
    survey = Survey.objects.filter(profile_id=request.session.get('profile_id')).latest('survey_created_at')
    request.session['survey_id'] = survey.survey_id

    response = requests.post('http://' + client_ip + f':5000/ai-total-recom/{survey.survey_id}/', 
                                headers={'X-CSRFToken': csrf_token,
                                        'Content-Type': 'application/json'})


    # flask 요청 받기
    contents = json.loads(response.text)
    request.session['contents'] = contents


    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("request_flask_total_recom function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:profile_total_report')




def recom_profile_total_report(request):

    start_time = time.time()

    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('/')

    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기> 영양 성분 리포트
    profile = Profile.objects.get(profile_id=request.session.get('profile_id'))
    survey = Survey.objects.get(survey_id=request.session.get('survey_id'))


    # 세션에서 contents 가져오기
    contents = request.session.get('contents', {})


    # 1) 추천 영양 성분 가져오기
    ## 영양 성분명, 주요건강기능, 일일 섭취량 상하한
    recom = Recom.objects.get(survey_id=survey.survey_id)
    recommended_ingredients = RecomIngredient.objects.filter(recom_id=recom.recom_id).values_list('ingredient_id', flat=True)
    recommended_ingredients = list(recommended_ingredients)
    recommended_ingredients = Ingredient.objects.filter(ingredient_id__in=recommended_ingredients)
    

    # 2) 영양 성분 리포트 바탕으로 영양제 추천
    ## recom_survey_product에서 데이터 가져오기
    recommended_products = RecomSurveyProduct.objects.filter(recom_id=recom.recom_id).values_list('product_id', flat=True)
    recommended_products = list(recommended_products)
    recommended_products = Product.objects.filter(product_id__in=recommended_products)

    
    # 3) 성별*연령 기반 영양제 추천
    ## 성별*연령별 기반 영양제
    sex_age_recommended_products = contents['recom_product_sex_age_list']
    sex_age_recommended_products = Product.objects.filter(product_id__in=sex_age_recommended_products)


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
    

    # 키
    if survey.survey_height == None:
        survey.survey_height = '미입력'


    # 몸무게
    if survey.survey_weight == None:
        survey.survey_weight = '미입력'


    # 기저질환
    disease_code_dict = survey.survey_disease_code
    disease_kr_list = []
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


    # 음주여부
    alcohol_code = survey.survey_alcohol_code
    alcohol_code = ComCode.objects.filter(com_code=alcohol_code).values_list('com_code_name', flat=True)
    alcohol_code = ''.join(list(alcohol_code))
    

    # 흡연여부
    smoking_code = survey.survey_smoking_code
    smoking_code = ComCode.objects.filter(com_code=smoking_code).values_list('com_code_name', flat=True)
    smoking_code = ''.join(list(smoking_code))


    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("recom_profile_total_report function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return render(request, 'recommends/recom_profile_report.html', {
        'profile': profile,
        'survey':survey,
        'recommended_ingredients': recommended_ingredients,
        'recommended_products': recommended_products[:3], # 영양 성분 리포트 바탕 추천 product
        'collabo_recommendation_products' : sex_age_recommended_products[:3], # 연령*성별 기반 추천
        'age': age,
        'allergy': allergy_kr_list,
        'disease': disease_kr_list,
        'alcohol': alcohol_code,
        'pregnancy': pregnancy_kr_code,
        'smoking': smoking_code
    })



def recom_products_nutri_base(request, nutri_num):
    
    start_time = time.time()

    # AI추천받기: 영양제 추천 목록(영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 기반)
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('/')
    
    # 프로필 및 survey 데이터 가져오기
    profile = Profile.objects.get(profile_id=request.session['profile_id'])
    survey = Survey.objects.get(survey_id=request.session['survey_id'])
    print(f'profile_id: {request.session["profile_id"]}')
    print(f'survey_id: {request.session["survey_id"]}')

    
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


    # 음주여부
    alcohol_code = survey.survey_alcohol_code
    alcohol_code = ComCode.objects.filter(com_code=alcohol_code).values_list('com_code_name', flat=True)
    alcohol_code = ''.join(list(alcohol_code))
    

    # 흡연여부
    smoking_code = survey.survey_smoking_code
    smoking_code = ComCode.objects.filter(com_code=smoking_code).values_list('com_code_name', flat=True)
    smoking_code = ''.join(list(smoking_code))


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
        'allergy': allergy_kr_list,
        'disease': disease_kr_list,
        'alcohol': alcohol_code,
        'pregnancy': pregnancy_kr_code,
        'recommend_ingredient': recommend_ingredient,
        'popular_products': popular_products,
        'page_flag': page_flag,
        'nutri_num': nutri_num,
    })



def recom_products_profile_base(request):

    start_time = time.time()
    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 리포트 기반)
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('/')

    profile = Profile.objects.get(profile_id=request.session['profile_id'])
    survey = Survey.objects.get(survey_id=request.session['survey_id'])


    # ai 추천 받은 후 추천해주는 제품의 product_id가 필요
    recommendation = Recom.objects.get(survey_id=survey.survey_id)
    recom_product_list = RecomSurveyProduct.objects.filter(recom_id=recommendation.recom_id).values_list('product_id', flat=True)
    recom_product_list = list(recom_product_list)

    popular_products = Product.objects.filter(product_id__in=recom_product_list)


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
     

    # 키
    if survey.survey_height == None:
        survey.survey_height = '미입력'


    # 몸무게
    if survey.survey_weight == None:
        survey.survey_weight = '미입력'


    # 기저질환
    disease_code_dict = survey.survey_disease_code
    disease_kr_list = []
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


    # 음주여부
    alcohol_code = survey.survey_alcohol_code
    alcohol_code = ComCode.objects.filter(com_code=alcohol_code).values_list('com_code_name', flat=True)
    alcohol_code = ''.join(list(alcohol_code))
    

    # 흡연여부
    smoking_code = survey.survey_smoking_code
    smoking_code = ComCode.objects.filter(com_code=smoking_code).values_list('com_code_name', flat=True)
    smoking_code = ''.join(list(smoking_code))


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
        'allergy': allergy_kr_list,
        'disease': disease_kr_list,
        'alcohol': alcohol_code,
        'smoking': smoking_code,
        'pregnancy': pregnancy_kr_code,
        'popular_products': popular_products,
        'page_flag': page_flag
    })



def request_flask_sex_age_recom(request):

    start_time = time.time()

    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('/')
    
    profile = Profile.objects.get(profile_id=request.session['profile_id'])
    survey = Survey.objects.filter(profile_id=profile.pk).latest('survey_created_at')
    
    # flask 요청 
    client_ip = request.META.get('REMOTE_ADDR', None)

    if client_ip != '127.0.0.1' and client_ip != os.environ.get('AWS_PUBLIC_IP'):
        client_ip = os.environ.get('AWS_PUBLIC_IP')
    
    csrf_token = get_token(request)
    response = requests.post('http://' + client_ip + f':5000/ai-sex-age-recom/{survey.survey_id}', 
                            #  data=json.dumps(content), 
                                headers={'X-CSRFToken': csrf_token,
                                        'Content-Type': 'application/json'})
    

    # flask 응답 받기
    contents = json.loads(response.text)
    print(f'flask에서 응답 받은 내용 출력: {contents}')


    request.session['contents'] = contents
    

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("request_flask_sex_age_recom function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:products_sex_age_base')



def recom_products_sex_age_base(request):
    
    start_time = time.time()

    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(나이 & 성별 기반)
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    user_id = request.session.get('_auth_user_id')

    if not user_id:
        return redirect('/')

    # 세션에서 contents 가져오기
    contents = request.session.get('contents', {})
    profile = Profile.objects.get(profile_id=request.session['profile_id'])
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
     

    # 키
    if survey.survey_height == None:
        survey.survey_height = '미입력'


    # 몸무게
    if survey.survey_weight == None:
        survey.survey_weight = '미입력'


    # 기저질환
    disease_code_dict = survey.survey_disease_code
    disease_kr_list = []
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


    # 음주여부
    alcohol_code = survey.survey_alcohol_code
    alcohol_code = ComCode.objects.filter(com_code=alcohol_code).values_list('com_code_name', flat=True)
    alcohol_code = ''.join(list(alcohol_code))
    

    # 흡연여부
    smoking_code = survey.survey_smoking_code
    smoking_code = ComCode.objects.filter(com_code=smoking_code).values_list('com_code_name', flat=True)
    smoking_code = ''.join(list(smoking_code))


    page_flag = '연령 및 성별 기반'


    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("recom_products_sex_age_base function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return render(request, 'recommends/recom_profile_product_list.html', {
        'profile': profile,
        'survey': survey,
        'age': age,
        'allergy': allergy_kr_list,
        'disease': disease_kr_list,
        'alcohol': alcohol_code,
        'pregnancy': pregnancy_kr_code,
        'smoking': smoking_code,
        'popular_products': popular_products,
        'page_flag': page_flag,
    })



def request_flask_recom_model_old(request, profile_id, survey_id):
    start_time = time.time()

    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('/')
    
    profile = Profile.objects.get(profile_id=profile_id)
    

    # flask 요청 
    client_ip = request.META.get('REMOTE_ADDR', None)

    if client_ip != '127.0.0.1' and client_ip != os.environ.get('AWS_PUBLIC_IP'):
        client_ip = os.environ.get('AWS_PUBLIC_IP')
    
    csrf_token = get_token(request)
    response = requests.post('http://' + client_ip + f':5000/ai-total-recom-old/{survey_id}', 
                                headers={'X-CSRFToken': csrf_token,
                                        'Content-Type': 'application/json'})
    

    # flask 요청 받기
    contents = json.loads(response.text)


    request.session['contents'] = contents
    

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_minutes = int(execution_time_seconds // 60)
    execution_seconds = int(execution_time_seconds % 60)
    print("request_flask_recom_model_old function Execution Time:", execution_minutes, "minutes", execution_seconds, "seconds")

    return redirect('recommends:profile_total_report', profile.profile_id, survey_id)