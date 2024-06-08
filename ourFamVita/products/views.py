from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum, Count
from users.models import (Profile
                        , Survey, SurveyFunction
                        , Product, ProductReview, ProductIngredient, ProductFunction, ProductLog
                        , Ingredient, FunctionCode)

# Create your views here.
def product_detail(request, product_id, profile_id):

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    # AI추천받기:영양제 상세보기
    # menu: 영양제 추천받기 > 영양 성분 리포트 > 영양제 추천 목록 > 영양제 상세보기
    # /products/{product-id}/{profile-id}
    profile = Profile.objects.get(profile_id=profile_id)
    product = Product.objects.get(pk=product_id)
    if product.product_rating_avg == 0.00:
        product.product_rating_avg = 0



    # 제품 영양 성분
    product_ingredients = ProductIngredient.objects.filter(product_id=product_id).values_list('ingredient_id', flat=True)
    product_ingredients = list(product_ingredients)
    product_ingredients = Ingredient.objects.filter(ingredient_id__in=product_ingredients)



    # 제품 기능
    product_function_list = ProductFunction.objects.filter(product_id=product_id).values_list('function_code', flat=True)
    product_function_list = list(product_function_list)
    product_functions = FunctionCode.objects.filter(function_code__in=product_function_list)
    product_functions = product_functions.exclude(function_code__in=['HF00', 'HF26']).values_list('function_code_name', flat=True)
    product_functions = list(product_functions)



    # profile의 댓글 데이터
    review = ProductReview.objects.filter(product_id=product_id, profile_id=profile_id).exists()
    if review:
        review = ProductReview.objects.filter(product_id=product_id, profile_id=profile_id).get()
    


    # 영양제 로그 데이터 생성 및 저장
    survey = Survey.objects.filter(profile_id=profile_id).latest('created_at')
    ProductLog.objects.create(survey_id=survey, 
                              profile_id=profile, 
                              product_id=product,
                              visited_at=timezone.now(),
                              product_log_id=None,
                              leaved_at=None,
                              product_log_duration=1)
    


    # 건강설문에서 선택한 건강기능 고민 import
    survey_function_list = SurveyFunction.objects.filter(survey_id=survey.survey_id)
    survey_function_list = survey_function_list.exclude(function_code__in=['HF00', 'HF26']).values_list('function_code', flat=True)
    survey_function_list = list(survey_function_list)
    survey_functions = FunctionCode.objects.filter(function_code__in=survey_function_list).values_list('function_code_name', flat=True)
    survey_functions = list(survey_functions)

    
    
    return render(request, 'products/product_detail.html', {
        'profile': profile,
        'product': product, 
        'product_ingredients': product_ingredients,
        'review': review,
        'product_functions': product_functions,
        'survey_function_list': survey_function_list,
        'survey_functions': survey_functions,
    })


def product_review(request, product_id, profile_id):
    profile = Profile.objects.get(profile_id=profile_id)
    product = Product.objects.get(product_id=product_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # 프로필 댓글 데이터 저장
        ProductReview.objects.create(product_review_rating=rating,
                                    product_review_content=comment,
                                    product_id=product,
                                    created_at=timezone.now(),
                                    modified_at=None,
                                    profile_id=profile)

        # 영양제 제품 평점 업데이트
        product_review = ProductReview.objects.filter(product_id=product_id)
        total_sum = product_review.aggregate(total_sum=Sum('product_review_rating'))['total_sum']
        total_count = product_review.aggregate(total_count=Count('product_review_rating'))['total_count']
        
        product = Product.objects.get(product_id=product_id)
        product.product_rating_cnt = total_count
        product.product_rating_avg = total_sum/total_count
        product.save()

        
    return redirect('products:products_detail', product.product_id, profile.profile_id)