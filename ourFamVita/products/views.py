from django.shortcuts import render

# Create your views here.
def product_detail(request):
    # AI추천받기:영양제 상세보기
    # menu: 영양제 추천받기 > 영양 성분 리포트 > 영양제 추천 목록 > 영양제 상세보기
    # /products/{product-id}/{profile-id}
    return render(request, 'products/product_detail.html')