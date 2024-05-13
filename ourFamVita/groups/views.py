from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Profile, Recommendation, ProductIngredient, Product, ProductLike, RecommendationIngredient, RecommendationProduct, Ingredient, SurveyFunction, FunctionCode

# Create your views here.
def group_main(request, profile_id):
    profile = Profile.objects.get(profile_id = profile_id)
    user = User.objects.get(custom_user_id = profile.custom_user_id.custom_user_id)
    recommendations_info = Recommendation.objects.filter(custom_user_id=user.custom_user_id).order_by('-created_at')
   
 
    functions_list = []
    ingredients_list = []
    products_list = []

    for recommendation in recommendations_info:
        # user 건강고민
        survey_functions = SurveyFunction.objects.filter(survey_id = recommendation.survey_id.survey_id)[:3]
        for survey_function in survey_functions:
            function_codes = FunctionCode.objects.get(function_code = survey_function.function_code.function_code)
            functions_list.append(function_codes)

        # user 추천 영양 성분
        recommendation_ingredients = RecommendationIngredient.objects.filter(recommendation_id = recommendation.recommendation_id)[:3]
        for recommendation_ingredient in recommendation_ingredients: 
            ingredients = Ingredient.objects.get(ingredient_id = recommendation_ingredient.ingredient_id.ingredient_id)
            ingredients_list.append(ingredients)

        # user 추천 영양제
        recommendation_products = RecommendationProduct.objects.filter(recommendation_id = recommendation.recommendation_id)[:3]
        for recommendation_product in recommendation_products: 
            products = Product.objects.get(product_id = recommendation_product.product_id.product_id)
            products_list.append(products)
        

    # user 좋아요 영양제
    product_likes = ProductLike.objects.filter(custom_user_id=user.custom_user_id).order_by('-created_at')[:3]   
    product_like_list = []
    for product_like in product_likes:
        product = Product.objects.get(product_id = product_like.product_id.product_id)
        product_like_list.append(product) 
      
    context = {'user': user, 'profile':profile,
                'functions_list': functions_list[:3],
                'ingredients_list': ingredients_list[:3],
                'products_list' : products_list[:3],
                'product_like_list' : product_like_list,                                 
                } 
    print(functions_list[:3])   
    return render(request, 'groups/main.html', context)


def group_detail(request, profile_id):
    profile = Profile.objects.get(profile_id = profile_id)
    user = User.objects.get(custom_user_id = profile.custom_user_id.custom_user_id)
    recommendations_info = Recommendation.objects.filter(custom_user_id=user.custom_user_id).order_by('-created_at').first()   
    
    # user 추천 영양제
    products_list = []
    recommendation_products = RecommendationProduct.objects.filter(recommendation_id = recommendations_info.recommendation_id)[:5]
    for recommendation_product in recommendation_products:
        products = Product.objects.get(product_id = recommendation_product.product_id.product_id)
        products_list.append(products)
        
    
    context = {'user': user, 'recommendations_info':recommendations_info, 'products':products, 'profile':profile, 
               'products_list':products_list,
    }
    return render(request, 'groups/detail.html', context)


def group_individual(request, profile_id, ingredient_id):
    profile = Profile.objects.get(profile_id = profile_id)
    user = User.objects.get(custom_user_id = profile.custom_user_id.custom_user_id)
    ingredient = Ingredient.objects.get(ingredient_id=ingredient_id)
    product_ingredients = ProductIngredient.objects.filter(ingredient_id=ingredient_id)[:5]
    products_list = []
    for product_ingredient in product_ingredients:

        # user 추천 영양제
        products = Product.objects.get(product_id = product_ingredient.product_id.product_id)
        products_list.append(products)
        
    context = {'user': user, 'profile':profile, 'ingredient':ingredient, 'products':products,
               'products_list':products_list,
    }
    return render(request, 'groups/individual.html', context)