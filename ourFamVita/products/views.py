from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.db.models import Sum, Count
from users.models import (Profile, Survey, ComCode
                        , Product, ProductReview, ProductIngredient, ProductView, ProductLike
                        , Ingredient)
import json
from django.contrib.auth.decorators import login_required


# Create your views here.
def product_detail(request, product_id):

    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('/')



    # AI추천받기:영양제 상세보기
    # menu: 영양제 추천받기 > 영양 성분 리포트 > 영양제 추천 목록 > 영양제 상세보기
    profile = Profile.objects.get(profile_id=request.session['profile_id'])
    product = Product.objects.get(pk=product_id)
    if product.product_rating_avg == 0.00:
        product.product_rating_avg = 0



    # 제품 영양 성분
    product_ingredients = ProductIngredient.objects.filter(product_id=product_id).values_list('ingredient_id', flat=True)
    product_ingredients = list(product_ingredients)
    product_ingredients = Ingredient.objects.filter(ingredient_id__in=product_ingredients)



    # 제품 기능
    total_product_function_code_list = list(product.product_function_code.keys())
    product_function_dict = product.product_function_code
    product_functions = []
    for code in total_product_function_code_list:
        if code in ['HF00', 'HF26']:
            continue
        elif product_function_dict[code]:
            product_functions.append(code)
    for idx, code in enumerate(product_functions):
        code = ComCode.objects.filter(com_code=code).values_list('com_code_name', flat=True)
        print(f'code: {code}, type: {type(code)}')
        product_functions[idx] = ''.join(list(code))
    


    # profile의 댓글 데이터
    
    review_profile = None  # 기본값 설정
    
    ## 다른 프로필의 리뷰도 볼 수 있게 수정 
    reviews = ProductReview.objects.filter(
        product_id=product_id, product_review_content__isnull=False, product_review_deleted_at__isnull=True
    ).exists()
    
    if reviews:
        reviews = ProductReview.objects.filter(
            product_id=product_id, product_review_content__isnull=False, product_review_deleted_at__isnull=True
        # ).exclude(
        #     product_review_content=""
        ).select_related('profile_id').order_by('-product_review_created_at')[:10]
        
        review_profile = ProductReview.objects.filter(
            profile_id=profile.profile_id, product_id=product_id, product_review_content__isnull=False, product_review_deleted_at__isnull=True
        ).first()
        
    # 영양제 로그 데이터 생성 및 저장
    survey = Survey.objects.filter(profile_id=profile.profile_id).latest('survey_created_at')
    ProductView.objects.create(survey_id=survey, 
                              profile_id=profile, 
                              product_id=product,
                              product_view_visited_at=timezone.now(),
                              product_view_id=None,
                              product_view_leaved_at=None,
                              product_view_duration=1)
    

    # 건강설문에서 선택한 건강기능 고민 import
    survey_functions = list(survey.survey_function_code.values())
    print()
    print(f'survey_functions: {survey_functions}')
    print()
    
    # 영양제 찜하기 객체 조회
    product_like = ProductLike.objects.filter(
        user_id=profile.user_id,
        profile_id=profile,
        product_id=product,
        product_like_deleted_at__isnull=True
    ).first()
    
    return render(request, 'products/product_detail.html', {
        'profile': profile,
        'product': product, 
        'product_ingredients': product_ingredients,
        'reviews': reviews,
        'review_profile': review_profile,
        'product_functions': product_functions,
        'survey_functions': survey_functions,
        'product_like': product_like,
    })

# 제품 리뷰 작성(생성)
@login_required
def product_review(request, product_id):
    profile = Profile.objects.get(profile_id=request.session.get('profile_id'))
    product = Product.objects.get(product_id=product_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # 프로필 리뷰 데이터 저장
        ProductReview.objects.create(product_review_rating=rating,
                                    product_review_content=comment,
                                    product_id=product,
                                    product_review_created_at=timezone.now(),
                                    product_review_modified_at=None,
                                    profile_id=profile)
        
        # 영양제 제품 평점 업데이트(삭제된 리뷰 제외)
        product_reviews = ProductReview.objects.filter(product_id=product_id, product_review_deleted_at__isnull=True)
        total_sum = product_reviews.aggregate(total_sum=Sum('product_review_rating'))['total_sum']
        total_count = product_reviews.aggregate(total_count=Count('product_review_rating'))['total_count']

        
        product = Product.objects.get(product_id=product_id)
        product.product_rating_cnt = total_count
        product.product_rating_avg = total_sum/total_count
        product.save()
        
    return redirect('products:products_detail', product.product_id)

# 제품 리뷰 삭제
@login_required
def product_review_delete(request, product_id, profile_id, product_review_id):
    review = get_object_or_404(ProductReview, pk=product_review_id, profile_id=profile_id)
    
    if request.method == 'POST':
        review.product_review_deleted_at = timezone.now()
        review.save()
        
    return redirect('products:products_detail', product_id=product_id)

# 영양제 찜하기
@login_required
def product_like(request, product_id):
    profile = Profile.objects.get(profile_id=request.session.get('profile_id'))
    product = Product.objects.get(product_id=product_id)

    # 현재 경로를 저장
    current_path = request.path
    print(f'current_path : {current_path}')
    
    # ProductLike 객체 확인 (profile_id와 product_id가 일치하고, product_like_deleted_at이 null인 경우)
    product_like = ProductLike.objects.filter(
        profile_id=profile,
        product_id=product,
        product_like_deleted_at__isnull=True
    ).first()
    
    if request.method == 'POST':
        # product_like 객체가 없으면 새로 생성
        if not product_like:
            product_like = ProductLike.objects.create(
                user_id=profile.user_id,
                profile_id=profile,
                product_id=product,
                product_like_page=current_path
            )
        else:
            # 이미 찜한 상태라면 찜 해제 처리
            product_like.product_like_deleted_at = timezone.now()
            product_like.save()

    return redirect('products:products_detail', product_id)