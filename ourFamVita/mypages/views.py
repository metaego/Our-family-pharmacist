import json
from django.shortcuts import render, redirect, get_object_or_404
# from users.models import Profile, ProductLog, Product, Recommendation, RecommendationIngredient, Ingredient, SurveyFunction, ProductLike, ProductReview, FunctionCode
from users.models import (Profile, Product, ProductView, ProductLike, ProductReview
                          , Survey
                          , ComCode
                          , Ingredient  
                          , Recom, RecomIngredient
                          )
from django.db.models import Max
# Create your views here.

def mypage_main(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)   
    context = {'profile': profile,
                  }
    return render(request, 'mypages/main.html', context)


# 최근 조회한 제품
def mypage_views(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)
    product_views = ProductView.objects.filter(profile_id=profile_id).order_by('-product_view_visited_at')[:10] 
    products_list = []

    # for productlog in productlogs: 
    for product_view in product_views:
        # product = Product.objects.get(product_id = productlog.product_id.product_id)
        product = Product.objects.get(product_id = product_view.product_id.product_id)
        products_list.append(product)
        # 최근 조회한 제품 중복 제거
        products_list = list(set(products_list))[:5]
        
    context =  {'profile': profile, 
                'products_list':products_list,
                }
    return render(request, 'mypages/views.html', context)


def mypage_recommends(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)     
    # recommendations_info = Recommendation.objects.filter(profile_id=profile_id).order_by('-created_at')[:5]
    recoms_info = Recom.objects.filter(profile_id=profile_id).order_by('-recom_created_at')[:5] # 최근 5개 추천 목록 
    ingredients_list = []

    # for recommendation in recommendations_info: 
    for recom in recoms_info: 
        ingredients_info = []
        functions_info = []
        # recommendation_ingredients = RecommendationIngredient.objects.filter(recommendation_id=recommendation.recommendation_id)
        recom_ingredients = RecomIngredient.objects.filter(recom_id=recom.recom_id)
        
        # for recommendation_ingredient in recommendation_ingredients:
        for recom_ingredient in recom_ingredients:
            # ingredient = Ingredient.objects.get(ingredient_id=recommendation_ingredient.ingredient_id.ingredient_id)
            ingredient = Ingredient.objects.get(ingredient_id=recom_ingredient.ingredient_id.ingredient_id)
            ingredients_info.append(ingredient)
        
        # survey에서 function code 불러오기  ----------------------------------------  
        # survey_functions = SurveyFunction.objects.filter(survey_id=recommendation.survey_id) 
        survey = Survey.objects.get(survey_id=recom.survey_id.survey_id)
        survey_function_code_dict = survey.survey_function_code # {'1st': 'HF07', '2nd': 'HF08'}
        
        # functions_info = list(survey_function_code_dict.values())  # ['HF07', 'HF08']
        
        for function_code in survey_function_code_dict.values():
            function_code_name = ComCode.objects.get(com_code=function_code).com_code_name
            functions_info.append(function_code_name)
        print(f'functions_info:{functions_info}')    
        # for survey_function in survey_functions:
        #     function_code = FunctionCode.objects.get(function_code = survey_function.function_code.function_code)
        #     functions_info.append(function_code)
    
        # info = [ingredients_info, functions_info, recommendation]
        info = [ingredients_info, functions_info, recom]
        
        ingredients_list.append(info)

    context = {
        'profile': profile,
        'ingredients_list': ingredients_list,
        # 'survey': survey,
    }
    return render(request, 'mypages/recommends.html', context)

# 영양제 찜하기 기능 구현 전
def mypage_likes(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id) 
    
    # 각 product_id별로 최신 product_like_created_at을 가지는 레코드 필터링
    latest_likes = ProductLike.objects.filter(
        profile_id=profile_id,
        product_like_deleted_at__isnull=True  # 삭제되지 않은 값만 필터링
    ).values('product_id').annotate(
        latest_like_date=Max('product_like_created_at')
    )

    # 최신 찜 날짜 기준으로 product_likes 필터링
    product_likes = ProductLike.objects.filter(
        profile_id=profile_id,
        product_like_deleted_at__isnull=True,
        product_like_created_at__in=[like['latest_like_date'] for like in latest_likes]
    ).select_related('product_id').order_by('-product_like_created_at')

    context = {'profile': profile,
               'product_likes':product_likes,                                
                  }
    return render(request, 'mypages/likes.html', context)    
     

def mypage_reviews(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id) 
    product_reviews = ProductReview.objects.filter(profile_id=profile_id, product_review_content__isnull=False).exists()
    if product_reviews:
    # 각 product_id 별로 최신 product_review_created_at을 가지는 레코드 필터링
        latest_reviews = ProductReview.objects.filter(
            profile_id=profile_id,
            product_review_content__isnull=False,
            product_review_deleted_at__isnull=True
        ).values('product_id').annotate(
            latest_review_date=Max('product_review_created_at')
        )
        
        # 최신 리뷰 날짜 기준으로 product_reviews 필터링
        product_reviews = ProductReview.objects.filter(
            profile_id=profile_id,
            product_review_content__isnull=False,
            product_review_deleted_at__isnull=True,
            product_review_created_at__in=[review['latest_review_date'] for review in latest_reviews]
        ).select_related('product_id').order_by('-product_review_created_at')
        
        print(f'product_reviews:{product_reviews}')
        
    context = {'profile': profile,
               'product_reviews': product_reviews,                                   
                  }
    
    return render(request, 'mypages/reviews.html', context)    

