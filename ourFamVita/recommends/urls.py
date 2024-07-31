from django.urls import path
from . import views

app_name = 'recommends'

urlpatterns = [
    # AI추천받기:나의 프로필 정보 확인
    # menu: ai 영양제 추천받기(profile_info)
    path('info/', views.recom_info, name='profile_info'),



    # 설문 조사 결과 저장
    path('survey_data/<int:survey_id>', views.save_survey_data, name='save_survey_data'),



    # AI추천받기: 나의 프로필 정보 확인
    # menu: ai 영양제 추천받기(profile_info)
    path('request_flask/report_base_total_recom/', views.request_flask_total_recom, name='request_flask_total_recom'),



    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트
    path('reports/', views.recom_profile_total_report, name='profile_total_report'),



    # AI추천받기: 영양제 추천 목록(추천받은 영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    path('<int:nutri_num>/nutri_base_products/', views.recom_products_nutri_base, name='products_nutri_base'),



    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    path('nutri_report_base_products/', views.recom_products_profile_base, name='products_profile_base'),



    # flask에 성별 & 연령별 영양제 추천
    path('request_flask/sex_age_base_product_recom/', views.request_flask_sex_age_recom, name='request_flask_sex_age_recom'),



    # AI추천받기: 영양제 추천 목록(나이 & 성별 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    path('sex_age_base_products/', views.recom_products_sex_age_base, name='products_collabo_base'),



    # flask에 데이터 신규 생성하지 않고 추천받기
    path('request_flask/old/<int:profile_id>/<int:survey_id>/', views.request_flask_recom_model_old, name='request_flask_recom_model_old')
]
