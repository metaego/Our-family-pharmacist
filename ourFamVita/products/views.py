from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum, Count
from users.models import (Profile, Survey, ComCode 
                        , Product, ProductReview, ProductIngredient, ProductView 
                        , Ingredient)
import json


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
    review = ProductReview.objects.filter(product_id=product_id, profile_id=profile.profile_id).exists()
    if review:
        review = ProductReview.objects.filter(product_id=product_id, profile_id=profile.profile_id).get()
    


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
    survey_functions = list(json.loads(survey.survey_function_code).values())
    
    

    return render(request, 'products/product_detail.html', {
        'profile': profile,
        'product': product, 
        'product_ingredients': product_ingredients,
        'review': review,
        'product_functions': product_functions,
        'survey_functions': survey_functions,
    })



def product_review(request, product_id):
    profile = Profile.objects.get(profile_id=request.session.get('profile_id'))
    product = Product.objects.get(product_id=product_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')



        # 프로필 댓글 데이터 저장
        ProductReview.objects.create(product_review_rating=rating,
                                    product_review_content=comment,
                                    product_id=product,
                                    product_review_created_at=timezone.now(),
                                    product_review_modified_at=None,
                                    profile_id=profile)
        


        # 영양제 제품 평점 업데이트
        product_reviews = ProductReview.objects.filter(product_id=product_id)
        total_sum = product_reviews.aggregate(total_sum=Sum('product_review_rating'))['total_sum']
        total_count = product_reviews.aggregate(total_count=Count('product_review_rating'))['total_count']
        
        product = Product.objects.get(product_id=product_id)
        product.product_rating_cnt = total_count
        product.product_rating_avg = total_sum/total_count
        product.save()

        
    return redirect('products:products_detail', product.product_id)