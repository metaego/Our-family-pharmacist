import json
from django.shortcuts import render, redirect, get_object_or_404
# from users.models import Profile, ProductLog, Product, Recommendation, RecommendationIngredient, Ingredient, SurveyFunction, ProductLike, ProductReview, FunctionCode
from users.models import (Profile, Product, ProductView, ProductLike, ProductReview
                          , Survey
                          , ComCode
                          , Ingredient  
                          , Recom, RecomIngredient
                          )

# Create your views here.

def mypage_main(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)   
    context = {'profile': profile,
                  }
    return render(request, 'mypages/main.html', context)



def mypage_views(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)
    # productlogs = ProductLog.objects.filter(profile_id=profile_id).order_by('-visited_at')[:5] 
    product_views = ProductView.objects.filter(profile_id=profile_id).order_by('-product_view_visited_at')[:5] 
    products_list = []

    # for productlog in productlogs: 
    for product_view in product_views:
        # product = Product.objects.get(product_id = productlog.product_id.product_id)
        product = Product.objects.get(product_id = product_view.product_id.product_id)
        products_list.append(product)
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
    # print(f'profile:{profile}')
    # product_likes = ProductLike.objects.filter(profile_id=profile_id).order_by('-created_at')[:5]
    product_likes = ProductLike.objects.filter(profile_id=profile_id).order_by('-product_like_created_at')[:5]
    # print(f'product_likes:{product_likes}')
    products_list = []
    for product_like in product_likes:
        product = Product.objects.get(product_id = product_like.product_id.product_id)
        # print(f'product:{product}')
        products_list.append(product)
    # print(f'products_list:{products_list}')
    context = {'profile': profile,
               'products_list':products_list,                                
                  }
    return render(request, 'mypages/likes.html', context)    
     

def mypage_reviews(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id) 
    # product_reviews = ProductReview.objects.filter(profile_id=profile_id).order_by('-created_at')[:5]
    product_reviews = ProductReview.objects.filter(profile_id=profile_id).order_by('-product_review_created_at')[:5]
    products_list = []
    for product_review in product_reviews:
        product = Product.objects.get(product_id = product_review.product_id.product_id)
        products_info= [product_review, product]
        products_list.append(products_info)
    
    context = {'profile': profile,
               'products_list':products_list,                                   
                  }
    return render(request, 'mypages/reviews.html', context)    

