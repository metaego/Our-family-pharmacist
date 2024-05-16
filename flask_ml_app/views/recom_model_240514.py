import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from .PillSoGoodModel import DataLoad, DataPreprocessor, RecommendModel
import os


def ai_total_recom(survey_df):
       # 추천을 받을 사용자 데이터셋 변수명 survey_df
       # 아래는 예시이기 때문에 DB에서 불러온 데이터로 survey_df 데이터셋을 지정해준다.
       # survey_df = pd.DataFrame({'survey_id' : [51787], 'user_id' : [51787], 'profile_id' : [51787], 'survey_age_group' : [20], 'survey_sex' : [0],
       #        'survey_pregnancy' : [0], 'survey_operation' : [0], 'survey_alcohol' : [0],
       #        'survey_smoking' : [1], 'HF00' : [0], 'HF01' : [1], 'HF02' : [0], 'HF03' : [0], 'HF04' : [0], 'HF05' : [0],
       #        'HF06' : [0], 'HF07' : [0], 'HF08' : [0], 'HF09' : [1], 'HF10' : [0], 'HF11' : [0], 'HF12' : [0], 'HF13' : [0], 'HF14' : [0],
       #        'HF15' : [0], 'HF16' : [0], 'HF17' : [0], 'HF18' : [0], 'HF19' : [0], 'HF20' : [0], 'HF21' : [0], 'HF22' : [0], 'HF23' : [0],
       #        'HF24' : [0], 'HF25' : [0], 'AL01' : [0], 'AL02' : [0], 'AL03' : [0], 'AL04' : [0], 'AL05' : [0],
       #        'AL06' : [0], 'AL07' : [0], 'AL08' : [1], 'AL09' : [0], 'AL10' : [0], 'AL11' : [0], 'AL12' : [0], 'AL13' : [0], 'AL14' : [0],
       #        'AL15' : [0], 'AL16' : [0], 'AL17' : [0], 'AL18' : [0], 'AL19' : [0], 'AL20' : [0], 'DI01' : [0], 'DI02' : [0], 'DI03' : [0],
       #        'DI04' : [0], 'DI05' : [0], 'DI06' : [0], 'DI07' : [0], 'DI08' : [0], 'DI09' : [0], 'DI10' : [0], 'DI11' : [0], 'DI12' : [0],
       #        'DI13' : [0], 'DI14' : [0], 'DI15' : [0], 'DI16' : [0], 'DI17' : [1]})

       # 추천 알고리즘에 필요한 데이터프레임 피클파일 저장 경로 설정
       # 상위 디렉토리
       parent_directory = r'flask_ml_app/views/data/'
       ingredient_df_path = parent_directory + r'recom_ingredient_dataset_fin_240515_v3.pkl' 
       product_df_path = parent_directory + r'product_df_preprocessed.pkl'
       dummy_survey_df_path = parent_directory + r'dummy_add_recom_ingredients_240513_v4.pkl'
       review_df_path = parent_directory + r'dummy_review_240510_vector_240512_v2.pkl'
       user_features_list_path = parent_directory + r'user_features_list.pkl'
       item_features_path = parent_directory + r'item_features.pkl'
       dataset_path = parent_directory + r'dataset.pkl'
       model_path = parent_directory + r'model.pkl'

       current_path = os.getcwd()
       print("현재 디렉토리 경로: ", current_path)
       print()
       # 추천 알고리즘에 필요한 데이터프레임 가져오기
       dataload_model = DataLoad(ingredient_df_path, product_df_path, dummy_survey_df_path, review_df_path, user_features_list_path, item_features_path, dataset_path, model_path)
       ingredient_df, product_df, dummy_survey_df, review_df, user_features_list, item_features, dataset, model = dataload_model.dataload()
       
       # 추천받을 사용자 및 유사 그룹 사용자 설문 데이터셋 - 전처리 및 두 데이터프레임을 합친다.
       profile_id, survey_df = DataPreprocessor(survey_df, dummy_survey_df).preprocess_data()

       # 추천모델
       recom_model = RecommendModel(survey_df, product_df, ingredient_df, profile_id, review_df, user_features_list, item_features, dataset, model)

       # 추천받을 사용자 인덱스와 행(시리즈)
       survey_idx, survey_row = recom_model.find_profile_id_row(survey_df, profile_id)

       # 추천 영양성분 TOP5 ingredient_id가 담긴 리스트(인덱스 순서대로 순위 ), 추천 영양성분 TOP5 데이터프레임
       # recom_ingredient_id_list에 있는 아이디 값을 가져가서 Djnago에서 활용한다.
       recom_ingredient_id_list, recom_top5_ingredient_df, survey_row = recom_model.run_recommend_ingredients_function()

       # recom_product_survey_list : 건강설문조사에 따른 추천 영양제 product_id가 담긴 리스트
       # recom_product_sex_age_list : 성별, 연령에 따른 추천 영양제 product_id가 담긴 리스트
       recom_product_survey_list, recom_product_sex_age_list= recom_model.recommendation_product_lfm(survey_row, recom_top5_ingredient_df)

       ###### 여기까지 2초 가량 소요됨 #########################
       
       # 추천 영양성분 top 5 리스트, 건강설문에 따른 추천 영양제 list, 성별*연령에 따른 추천 영양제 list
       return recom_ingredient_id_list, recom_product_survey_list[:20], recom_product_sex_age_list[:20]