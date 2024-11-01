from flask import Blueprint# ,  url_for # render_template
from flask import jsonify, request# , redirect, 
import os
import time
import pymysql
import pandas as pd
from dotenv import load_dotenv
from .recom_model_240514 import ai_total_recom 
from datetime import datetime
import json
# from werkzeug.utils import redirect

bp = Blueprint('ai-total-recom', __name__, url_prefix='/ai-total-recom')

@bp.route('/<int:survey_id>/', methods=['POST'])
def flask_ai_total_recom(survey_id):
    # ai 추천 결과 DB에 저장
    start_time = time.time()
    load_dotenv()    

    # mysql과 flask 연동
    db = pymysql.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        port=int(os.environ.get('MYSQL_PORT')),
        # db='ourFamVitaDBNew',
        db=os.environ.get('MYSQL_DATABASE_NAME'),
        charset='utf8mb4'
)
    # data = request.get_json()
    # print(f'flask에서 받은 data 출력: {data}')
    # survey_id = data['survey_id']

    
     # 1-1) db에서 필요한 데이터 불러오기
    query = f'''select survey_id, survey_age_group, survey_sex, survey_pregnancy_code, survey_operation_code, survey_alcohol_code, survey_smoking_code, \
            survey_allergy_code, survey_disease_code, \
            survey_function_code, user_id, profile_id \
            from survey where survey_id="{survey_id}"'''
    cursor = db.cursor(pymysql.cursors.DictCursor)  # Dict 타입으로 받기
    cursor.execute(query)
    survey_data = cursor.fetchone()

    print()
    print(f'survey_data: {survey_data}')
    print()
    
    survey_data['survey_allergy_code'] = json.loads(survey_data['survey_allergy_code'])
    survey_data['survey_disease_code'] = json.loads(survey_data['survey_disease_code'])
    survey_data['survey_function_code'] = json.loads(survey_data['survey_function_code'])
    # print()
    # print(f"survey_data['survey_function_code']: {survey_data['survey_function_code']}")
    # print(f"type(survey_data['survey_function_code']): {type(survey_data['survey_function_code'])}")
    # print()

    # 1-2) 데이터 전처리
    if survey_data["survey_sex"] == 'm':
        survey_data["survey_sex"] = 0
    else:
        survey_data["survey_sex"] = 1

    if survey_data["survey_age_group"] in ['6~8세', '9~11세', '어린이']:
        survey_data["survey_age_group"] = 0
    elif survey_data["survey_age_group"] in ['12~14세', '15~18세', '청소년']:
        survey_data["survey_age_group"] = 10
    elif survey_data["survey_age_group"] == '20대':
        survey_data["survey_age_group"] = 20
    elif survey_data["survey_age_group"] == '30대':
        survey_data["survey_age_group"] = 30
    elif survey_data["survey_age_group"] == '40대':
        survey_data["survey_age_group"] = 40
    elif survey_data["survey_age_group"] == '50대':
        survey_data["survey_age_group"] = 50
    elif survey_data["survey_age_group"] in ['60대', '60세 이상']:
        survey_data["survey_age_group"] = 60

    if survey_data["survey_pregnancy_code"] != 'P0':
        survey_data["survey_pregnancy_code"] = 1
    else:
        survey_data["survey_pregnancy_code"] = 0

    if survey_data["survey_operation_code"] in ['O0', 'O9']:
        survey_data["survey_operation_code"] = 0
    else:
        survey_data["survey_operation_code"] = 1
    
    if survey_data["survey_alcohol_code"] == 'A3':
        survey_data["survey_alcohol_code"] = 1
    else:
        survey_data["survey_alcohol_code"] = 0

    if survey_data["survey_smoking_code"] == 'y':
        survey_data["survey_smoking_code"] = 1
    else:
        survey_data["survey_smoking_code"] = 0

    

    # 2) survey_df 생성
    survey_df = pd.DataFrame({'survey_id' : [int(survey_data["survey_id"])], 'user_id' : [int(survey_data["user_id"])], 'profile_id' : [int(survey_data["profile_id"])], 'survey_age_group' : [survey_data["survey_age_group"]], 'survey_sex' : [survey_data["survey_sex"]],
              'survey_pregnancy' : [survey_data["survey_pregnancy_code"]], 'survey_operation' : [survey_data["survey_operation_code"]], 'survey_alcohol' : [survey_data["survey_alcohol_code"]],
              'survey_smoking' : [survey_data["survey_smoking_code"]], 'HF00' :[0] , 'HF01' : [0], 'HF02' : [0], 'HF03' : [0], 'HF04' : [0], 'HF05' : [0],
              'HF06' : [0], 'HF07' : [0], 'HF08' : [0], 'HF09' : [0], 'HF10' : [0], 'HF11' : [0], 'HF12' : [0], 'HF13' : [0], 'HF14' : [0],
              'HF15' : [0], 'HF16' : [0], 'HF17' : [0], 'HF18' : [0], 'HF19' : [0], 'HF20' : [0], 'HF21' : [0], 'HF22' : [0], 'HF23' : [0],
              'HF24' : [0], 'HF25' : [0], 'AL01' : [0], 'AL02' : [0], 'AL03' : [0], 'AL04' : [0], 'AL05' : [0],
              'AL06' : [0], 'AL07' : [0], 'AL08' : [0], 'AL09' : [0], 'AL10' : [0], 'AL11' : [0], 'AL12' : [0], 'AL13' : [0], 'AL14' : [0],
              'AL15' : [0], 'AL16' : [0], 'AL17' : [0], 'AL18' : [0], 'AL19' : [0], 'AL20' : [0], 'DI01' : [0], 'DI02' : [0], 'DI03' : [0],
              'DI04' : [0], 'DI05' : [0], 'DI06' : [0], 'DI07' : [0], 'DI08' : [0], 'DI09' : [0], 'DI10' : [0], 'DI11' : [0], 'DI12' : [0],
              'DI13' : [0], 'DI14' : [0], 'DI15' : [0], 'DI16' : [0], 'DI17' : [0]})

    for codes in survey_data["survey_allergy_code"]["ALLERGY"]:
        for code in codes:
            if code in survey_df.columns:
                survey_df[code] = 1

    for codes in survey_data["survey_disease_code"]["DISEASE"]:
        for code in codes:
            if code in survey_df.columns:
                survey_df[code] = 1

    for code in list(survey_data["survey_function_code"].values()):
        if code in survey_df.columns:
            survey_df[code] = 1


    # 3) ai 모델 실행
    recom_ingredient_id_list, recom_product_survey_list, recom_product_sex_age_list = ai_total_recom(survey_df)
    

    # print(f'survey_data["survey_id"]: {survey_data["survey_id"]}')
    # print()
    # print(f'recom_product_survey_list: {recom_product_survey_list[:10]}')
    # print()
    # print(f'recom_product_sex_age_list: {recom_product_sex_age_list[:10]}')

    # 4) 실행 결과 db insert
    # 현재 날짜와 시간을 MySQL datetime 형식으로 변환
    # recommendation table에 데이터 insert
    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = 'insert into recom (recom_id, recom_created_at, user_id, profile_id, survey_id) \
                values (NULL, %s, %s, %s, %s)'
    cursor = db.cursor()
    cursor.execute(query, (formatted_datetime, survey_data["user_id"], survey_data["profile_id"], survey_data["survey_id"]))
    # db.commit()

    # recommendation pk 가져오기
    query = f'select recom_id from recom where survey_id = {survey_data["survey_id"]}'
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    recom_id_dict = cursor.fetchone()
    # print(f'recommendation_id: {recommendation_id}')
    # print()

    # recommendation_ingredient(top5)에 데이터 insert
    query = "INSERT INTO recom_ingredient (recom_ingredient_id, ingredient_id, recom_id) VALUES (NULL, %s, %s)"
    values = [(int(ingredient_id), recom_id_dict["recom_id"]) for ingredient_id in recom_ingredient_id_list]
    
    cursor = db.cursor()
    cursor.executemany(query, values)
    # db.commit()

    # recommendation_product에 데이터 insert
    for recom_product in recom_product_survey_list:
        query = "INSERT INTO recom_survey_product (recom_survey_product_id, product_id, recom_id) VALUES (NULL, %s, %s)"
        cursor.execute(query, (int(recom_product), recom_id_dict["recom_id"]))
    
    db.commit()
    db.close()



    # 5) 필요한 내용 장고에 return
    response_data = {
        'message' : '응답성공!',
        'profileid' : survey_data["profile_id"],
        'surveyid' : survey_data["survey_id"],
        'recom_ingredient_id_list': recom_ingredient_id_list,
        'recom_product_survey_list': recom_product_survey_list,
        'recom_product_sex_age_list': recom_product_sex_age_list
    }
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    return jsonify(response_data)