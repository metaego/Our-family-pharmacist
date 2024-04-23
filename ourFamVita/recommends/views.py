from django.shortcuts import render

# Create your views here.
def recom_info(request):
    # ai 추천받기: 나의 프로필 정보 확인
    # ai 영양제 추천받기 전 나의 프로필 정보 확인 페이지
    # /recommends/{profile-id}/info
    return render(request, 'recommends/recom_profile_info.html')

def recom_profile_total_report(request):
    # AI추천받기: 영양 성분 리포트
    # menu: ai 영양제 추천받기> 영양 성분 리포트
    # /recommends/{profile-id}/surveys/{survey-id}
    return render(request, 'recommends/recom_profile_report.html')


def recom_products_nutri_base(request):
    # AI추천받기: 영양제 추천 목록(영양 성분 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-nut-products/{nutri-num}
    return render(request, 'recommends/recom_profile_product_list.html')


def recom_products_profile_base(request):
    # AI추천받기: 영양제 추천 목록(영양 성분 리포트 기반)
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(영양 성분 리포트 기반)
    # /recommends/{profile-id}/surveys/{survey-id}/rec-total-products/
    return render(request, 'recommends/recom_profile_product_list.html')


def recom_products_collabo_base(request):
    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록(나이 & 성별 기반)
    # menu: home main(나이 & 성별 기반) > 영양제 추천 목록
    # /recommends/{profile-id}/surveys/{survey-id}/rec-products/
    return render(request, 'recommends/recom_profile_product_list.html')