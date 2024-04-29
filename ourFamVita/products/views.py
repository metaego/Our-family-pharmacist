from django.shortcuts import render
from users.models import Product, ProductReview

# Create your views here.
def product_detail(request, product_id, profile_id):
    # AI추천받기:영양제 상세보기
    # menu: 영양제 추천받기 > 영양 성분 리포트 > 영양제 추천 목록 > 영양제 상세보기
    # /products/{product-id}/{profile-id}
    product = Product.objects.get(pk=product_id)
    review = ProductReview.objects.filter(product_id=product_id).get(profile_id=profile_id)
    return render(request, 'products/product_detail.html', {
        'product': product, 
        'review':review
    })