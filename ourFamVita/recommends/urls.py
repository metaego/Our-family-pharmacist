from django.urls import path
from . import views

app_name = 'recommends'

urlpatterns = [
    # AI추천받기:나의 프로필 정보 확인
    # menu: ai 영양제 추천받기
    # /recommends/{profile-id}/info
    path('profile-id/info/', views.recom_info, name='profile_info'),
    
    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트
    # /recommends/{profile-id}/surveys/{survey-id}
    path('profile_id/surveys/survey_id/', views.recom_profile_total_report, name='profile_total_report'),
    
    # AI추천받기: 영양제 추천 목록(추천받은 영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # /recommends/{profile-id}/surveys/{survey-id}/rec-nut-products/{nutri-num}
    path('profile_id/surveys/survey_id/rec_nut_products/nutri_num/', views.recom_products_nutri_base, name='products_nutri_base'),
    
    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # /recommends/{profile-id}/surveys/{survey-id}/rec-total-products/
    path('profile_id/surveys/survey_id/rec_total_products/', views.recom_products_profile_base, name='products_profile_base'),

    # AI추천받기: 영양제 추천 목록(나이 & 성별 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    # /recommends/{profile-id}/surveys/{survey-id}/rec-collabo-products/
    path('profile_id/surveys/survey_id/rec_collabo_products/', views.recom_products_collabo_base, name='products_collabo_base')
]
