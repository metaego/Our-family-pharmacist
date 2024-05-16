from flask import Blueprint# ,  url_for # render_template
from flask import jsonify, request# , redirect, 
import os
import time
import pymysql
import pandas as pd
from dotenv import load_dotenv
from .recom_model_240514 import ai_total_recom 
from datetime import datetime


bp = Blueprint('main', __name__, url_prefix='/')
@bp.route('/ai-collabo-recom/<int:survey_id>/', methods=['POST'])
def flask_age_sex_base_ai_recom(survey_id):
    start_time = time.time()
    load_dotenv()    

    # mysql과 flask 연동
    db = pymysql.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        # db='testDB',
        db='ourFamVitaDBNew',
        charset='utf8mb4'
    )

     # 1) db에서 필요한 데이터 불러오기
    query = f'select survey_id, survey_age_group, survey_sex, survey_pregnancy_code, survey_operation_code, survey_alcohol_code, survey_smoke, \
            custom_user_id, profile_id from survey where survey_id="{survey_id}"'
    cursor = db.cursor(pymysql.cursors.DictCursor)  # Dict 타입으로 받기
    cursor.execute(query)
    survey_data = cursor.fetchone()
    print(f'survey_data: {survey_data}')
    print()

    query = f'select function_code from survey_function where survey_id = {survey_id}'
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    survey_function_data = cursor.fetchall()
    print(f'survey_function_data: {survey_function_data}')
    print()

    query = f'select allergy_code from survey_allergy where survey_id = {survey_id}'
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    survey_allergy_data = cursor.fetchall()
    print(f'survey_allergy_data: {survey_allergy_data}')
    print()

    query = f'select disease_code from survey_disease where survey_id = {survey_id}'
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    survey_disease_data = cursor.fetchall()
    print(f'survey_disease_data: {survey_disease_data}')
    print()
   
    data = survey_function_data + survey_allergy_data + survey_disease_data
    print(f'data: {data}')

    
    print(f'survey_data["survey_sex"]: {survey_data["survey_sex"]}')    
    # 1-1) 데이터 전처리
    if survey_data["survey_sex"] == 'm':
        survey_data["survey_sex"] = 0
    else:
        survey_data["survey_sex"] = 1

    if survey_data["survey_age_group"] in ['6~8세', '9~11세']:
        survey_data["survey_age_group"] = 0
    elif survey_data["survey_age_group"] in ['12~14세', '15~18세']:
        survey_data["survey_age_group"] = 10
    elif survey_data["survey_age_group"] == '20대':
        survey_data["survey_age_group"] = 20
    elif survey_data["survey_age_group"] == '30대':
        survey_data["survey_age_group"] = 30
    elif survey_data["survey_age_group"] == '40대':
        survey_data["survey_age_group"] = 40
    elif survey_data["survey_age_group"] == '50대':
        survey_data["survey_age_group"] = 50
    elif survey_data["survey_age_group"] in ['60대']:
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

    if survey_data["survey_smoke"] == 'y':
        survey_data["survey_smoke"] = 1
    else:
        survey_data["survey_smoke"] = 0

    

    # 2) survey_df 생성
    survey_df = pd.DataFrame({'survey_id' : [int(survey_data["survey_id"])], 'user_id' : [int(survey_data["custom_user_id"])], 'profile_id' : [int(survey_data["profile_id"])], 'survey_age_group' : [survey_data["survey_age_group"]], 'survey_sex' : [survey_data["survey_sex"]],
              'survey_pregnancy' : [survey_data["survey_pregnancy_code"]], 'survey_operation' : [survey_data["survey_operation_code"]], 'survey_alcohol' : [survey_data["survey_alcohol_code"]],
              'survey_smoking' : [survey_data["survey_smoke"]], 'HF00' :[0] , 'HF01' : [0], 'HF02' : [0], 'HF03' : [0], 'HF04' : [0], 'HF05' : [0],
              'HF06' : [0], 'HF07' : [0], 'HF08' : [0], 'HF09' : [0], 'HF10' : [0], 'HF11' : [0], 'HF12' : [0], 'HF13' : [0], 'HF14' : [0],
              'HF15' : [0], 'HF16' : [0], 'HF17' : [0], 'HF18' : [0], 'HF19' : [0], 'HF20' : [0], 'HF21' : [0], 'HF22' : [0], 'HF23' : [0],
              'HF24' : [0], 'HF25' : [0], 'AL01' : [0], 'AL02' : [0], 'AL03' : [0], 'AL04' : [0], 'AL05' : [0],
              'AL06' : [0], 'AL07' : [0], 'AL08' : [0], 'AL09' : [0], 'AL10' : [0], 'AL11' : [0], 'AL12' : [0], 'AL13' : [0], 'AL14' : [0],
              'AL15' : [0], 'AL16' : [0], 'AL17' : [0], 'AL18' : [0], 'AL19' : [0], 'AL20' : [0], 'DI01' : [0], 'DI02' : [0], 'DI03' : [0],
              'DI04' : [0], 'DI05' : [0], 'DI06' : [0], 'DI07' : [0], 'DI08' : [0], 'DI09' : [0], 'DI10' : [0], 'DI11' : [0], 'DI12' : [0],
              'DI13' : [0], 'DI14' : [0], 'DI15' : [0], 'DI16' : [0], 'DI17' : [0]})

    # 2-2) survey_df에 필요한 데이터(survey data) input
    for item in data:
        for values in item.values():
            if values in survey_df.columns:
                survey_df[values] = 1



    # 3) ai 모델 실행
    _, _, recom_product_sex_age_list = ai_total_recom(survey_df)
    


    # 4) 필요한 내용 장고에 return
    response_data = {
        'message' : '응답성공!',
        'profile_id' : survey_data["profile_id"],
        'survey_id' : survey_data["survey_id"],
        'recom_product_sex_age_list': recom_product_sex_age_list
    }
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")



    return jsonify(response_data)







# # if __name__ == '__main__':
# #     survey_id = 28205
# #     flask_ai_total_recom(survey_id)


# #     return redirect( 'http://' + os.environ.get('AWS_PUBLIC_IP') + ':8000/')
# #     return redirect(url_for('question._list'))

# #     question = Question.query.get_or_404(question_id)
# #     return render_template('question/question_detail.html', question=question)