from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # AI추천받기: 영양제 추천 목록
    # menu: ai 영양제 추천받기(profile_info) > 영양 성분 리포트 > 영양제 추천 목록 > 영양제 상세보기
    # /products/{product-id}/{profile-id}
    path('<int:product_id>/', views.product_detail, name='products_detail'),

    # 영양제 제품 리뷰 작성(생성)
    # /products/{product-id}/reviews/{profile-id}/{review-id}
    path('<int:product_id>/reviews/', views.product_review, name='product_review'),
    
    # 영양제 제품 리뷰 삭제
    # /products/{product-id}/reviews/{profile-id}/{review-id}
    path('<int:product_id>/reviews/<int:profile_id>/<int:product_review_id>/', views.product_review_delete, name='product_review_delete'),
    
    # 영양제 제품 찜하기
    # /products/{product-id}/likes/
    path('<int:product_id>/likes/', views.product_like, name='product_like'),
]
