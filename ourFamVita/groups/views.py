from django.shortcuts import render, redirect, get_object_or_404
from users.models import (Profile, Product, ProductView, ProductLike, ProductReview
                          , ProductIngredient
                          , Survey, SurveyComCode
                          , ComCode
                          , Ingredient  
                          , Recom, RecomIngredient, RecomSurveyProduct
                          , User
                          )
from django.db.models import OuterRef, Subquery
# from users.models import User, Profile, Recommendation, ProductIngredient, Product, ProductLike, RecommendationIngredient, RecommendationProduct, Ingredient, SurveyFunction, FunctionCode

# Create your views here.
def group_main(request, profile_id):
    profile = Profile.objects.get(profile_id=profile_id)
    user = User.objects.get(user_id=profile.user_id.user_id)
    recommendations_info = Recom.objects.filter(user_id=user.user_id).order_by('-recom_created_at')[:50]
    
    # 가족 최근 건강고민
    check_profile = {}
    for recom in recommendations_info:
        if recom.profile_id not in check_profile:
            check_profile[recom.profile_id.profile_id] = 0
            
    print(check_profile)
    
    latest_surveys = []
    for profile_id in check_profile.keys():
        latest_profile_recoms = Recom.objects.filter(profile_id=profile_id).order_by('-recom_created_at')[:3]
        for latest_profile_recom in latest_profile_recoms:
            latest_surveys.append(latest_profile_recom.survey_id)
    print(latest_surveys) 
    
    check_function_dict = {}
    check_functions = []
    for survey in latest_surveys:
        print(survey, survey.survey_function_code.values())
        for function_code in survey.survey_function_code.values():
            if function_code != 'HF00':
                if function_code not in check_functions:
                    check_functions.append(function_code)
                    check_function_dict[function_code] = 1
                else:
                    check_function_dict[function_code] += 1
    check_function_dict = dict(sorted(check_function_dict.items(), key=lambda x: x[1], reverse=True))
    
    group_latest_functions = list(check_function_dict.keys())[:5]
    
    #
    
    functions_list = []
    ingredients_list = []
    products_list = []
    
    for f in group_latest_functions:
        functions = ComCode.objects.get(com_code=f)
        functions_list.append(functions)
        
    print(functions_list)
    #

    for recommendation in recommendations_info:
        # # user 건강고민
        # survey_functions = SurveyComCode.objects.filter(com_code_grp='FUNCTION').filter(survey_id=recommendation.survey_id.survey_id)[:6]
        # for survey_function in survey_functions:
        #     function_code = ComCode.objects.get(com_code=survey_function.com_code.com_code)
        #     if function_code.com_code != 'HF00':
        #         functions_list.append(function_code)
        

        # user 추천 영양 성분
        recommendation_ingredients = RecomIngredient.objects.filter(recom_id = recommendation.recom_id)[:3]
        for recommendation_ingredient in recommendation_ingredients: 
            ingredient = Ingredient.objects.get(ingredient_id = recommendation_ingredient.ingredient_id.ingredient_id)
            ingredients_list.append(ingredient)

        # user 추천 영양제
        recommendation_products = RecomSurveyProduct.objects.filter(recom_id = recommendation.recom_id)[:3]
        for recommendation_product in recommendation_products: 
            product = Product.objects.get(product_id = recommendation_product.product_id.product_id)
            products_list.append(product)
        
    
    # user 좋아요 영양제
    product_likes = ProductLike.objects.filter(
        user_id=user.user_id, product_like_deleted_at__isnull=True
    ).select_related('product_id').order_by('-product_like_created_at')[:3]   
    
    # product_like_list = []
    # for product_like in product_likes:
    #     product = Product.objects.get(product_id = product_like.product_id.product_id)
    #     product_like_list.append(product) 
      
    context = { 'profile':profile,
                'functions_list': functions_list,
                'ingredients_list': ingredients_list[:3],
                'products_list' : products_list[:3],
                'product_likes' : product_likes,  
                'group_latest_functions' : group_latest_functions                               
                } 
   
    return render(request, 'groups/main.html', context)


def group_detail(request, profile_id):
    profile = Profile.objects.get(profile_id = profile_id)
    user = User.objects.get(user_id = profile.user_id.user_id)
    recommendations_info = Recom.objects.filter(user_id=user.user_id).order_by('-recom_created_at').first()   
    
    # user 추천 영양제
    products_list = []
    recommendation_products = RecomSurveyProduct.objects.filter(recom_id = recommendations_info.recom_id)
    for recommendation_product in recommendation_products:
        product = Product.objects.get(product_id = recommendation_product.product_id.product_id)
        products_list.append(product)
        
    context = {'profile':profile, 
               'products_list':products_list,
    }
    return render(request, 'groups/detail.html', context)


def group_individual(request, profile_id, ingredient_id):
    profile = Profile.objects.get(profile_id=profile_id)
    ingredient = Ingredient.objects.get(ingredient_id=ingredient_id)
    product_ingredients = ProductIngredient.objects.filter(ingredient_id=ingredient_id)[:5]
    products_list = []
    for product_ingredient in product_ingredients:

        # user 추천 영양제
        product = Product.objects.get(product_id=product_ingredient.product_id.product_id)
        products_list.append(product)
        
    context = { 'profile':profile,
                'ingredient':ingredient, 
               'products_list':products_list,
    }
    return render(request, 'groups/individual.html', context)