from django.urls import path
from . import views

app_name = 'recommends'

urlpatterns = [
    # AI추천받기:나의 프로필 정보 확인
    # menu: ai 영양제 추천받기(profile_info)
    # /recommends/{profile-id}/info
    # path('<int:profile_id>/info/', views.recom_info, name='profile_info'),
    path('info/', views.recom_info, name='profile_info'),

    # 설문 조사 결과 저장
    path('survey_id/<int:profile_id>/<int:survey_id>', views.save_survey_data, name='save_survey_data'),
    # AI추천받기: 나의 프로필 정보 확인
    # menu: ai 영양제 추천받기(profile_info)
    # /recommends/request_flask/{profile_id}/{survey_id}
    path('request_flask/<int:profile_id>/<int:survey_id>', views.request_flask_recom_model, name='request_flask_recom_model'),
    
    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트
    # /recommends/{profile-id}/surveys/{survey-id}
    path('<int:profile_id>/surveys/<int:survey_id>/', views.recom_profile_total_report, name='profile_total_report'),
    
    # AI추천받기: 영양제 추천 목록(추천받은 영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # /recommends/{profile-id}/surveys/{survey-id}/rec-nut-products/{nutri-num}
    path('<int:profile_id>/surveys/<int:survey_id>/rec_nut_products/<int:nutri_num>/', views.recom_products_nutri_base, name='products_nutri_base'),
    
    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # /recommends/{profile-id}/surveys/{survey-id}/rec-total-products/
    path('<int:profile_id>/surveys/<int:survey_id>/rec_total_products/', views.recom_products_profile_base, name='products_profile_base'),


    path('request_flask/collabo_recom/<int:profile_id>/', views.request_flask_collabo_recom_model, name='request_flask_collabo_recom_model'),

    # AI추천받기: 영양제 추천 목록(나이 & 성별 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    # /recommends/{profile-id}/rec-collabo-products/
    path('<int:profile_id>/rec_collabo_products/', views.recom_products_collabo_base, name='products_collabo_base'),

    # flask에 데이터 신규 생성하지 않고 추천받기
    path('request_flask/old/<int:profile_id>/<int:survey_id>/', views.request_flask_recom_model_old, name='request_flask_recom_model_old')
]
