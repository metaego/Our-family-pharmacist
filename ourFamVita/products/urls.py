from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 > 영양제 상세보기
    # /products/{product-id}/{profile-id}
    path('<int:product_id>/<int:profile_id>/', views.product_detail, name='products_detail'),
]
