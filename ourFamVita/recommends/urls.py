from django.urls import path
from . import views

app_name = 'recommends'

urlpatterns = [
    # AI추천받기:나의 프로필 정보 확인
    # menu: ai 영양제 추천받기(profile_info)
    # 기능: 추천받기 전 "AI영양제추천받기"화면에서 나의 프로필 정보 조회
    path('info/', views.recom_info, name='profile_info'),



    # 기능: 건강 설문(관심있는 건강기능) 정보를 DB에 저장
    path('survey_data/<int:survey_id>/', views.save_survey_data, name='save_survey_data'),



    # AI추천받기: 나의 프로필 정보 확인
    # menu: ai 영양제 추천받기(profile_info)
    # 기능: flask에 ai 추천 요청 보내기
    path('request_flask/report_base_total_recom/', views.request_flask_total_recom, name='request_flask_total_recom'),



    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트
    # 기능: flask에서 추천받은 "영양 성분 리포트"화면 조회
    path('reports/', views.recom_profile_total_report, name='profile_total_report'),



    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # 기능: "영양 성분 리포트"화면에서 특정 영양성분 추천 영양제 리스트 조회 
    path('<int:nutri_num>/nutri_base_products/', views.recom_products_nutri_base, name='products_nutri_base'),



    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # 기능: "영양 성분 리포트"화면에서 영양성분 리포트 바탕 추천 영양제 리스트 조회
    path('nutri_report_base_products/', views.recom_products_profile_base, name='products_profile_base'),



    # 기능: flask에 성별 & 연령별 영양제 추천 요청 보내기
    path('request_flask/sex_age_base_product_recom/', views.request_flask_sex_age_recom, name='request_flask_sex_age_recom'),



    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # menu: home main(성별 & 연령별 기반) > 영양제 추천 목록
    # 기능: flask에서 추천받은 성별 & 연령별 기반 추천 영양제 리스트 조회
    path('sex_age_base_products/', views.recom_products_sex_age_base, name='products_sex_age_base'),



    # flask에 데이터 신규 생성하지 않고 추천받기
    path('request_flask/old/<int:profile_id>/<int:survey_id>/', views.request_flask_recom_model_old, name='request_flask_recom_model_old')
]
