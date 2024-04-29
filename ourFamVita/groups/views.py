from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Recommendation, ProductIngredient, Product, ProductLike, RecommendationIngredient, RecommendationProduct, Ingredient, SurveyFunction

# Create your views here.
def group_main(request, user_id):
    user = get_object_or_404(User, custom_user_id=user_id)
    # profiles = get_object_or_404(Profile, custom_user_id=user_id)
    recommendations_info = Recommendation.objects.filter(custom_user_id=user_id).order_by('-created_at')
    recommendations_info = get_object_or_404(recommendations_info)

    # user 건강고민
    survey_functions = SurveyFunction.objects.filter(survey_id = recommendations_info.survey_id)[:5] 

    # user 추천 영양 성분
    recommendation_ingredients = RecommendationIngredient.objects.filter(recommendation_id = recommendations_info.recommendation_id)
    recommendation_ingredients = get_object_or_404(recommendation_ingredients)
    ingredients = Ingredient.objects.filter(ingredient_id = recommendation_ingredients.ingredient_id.ingredient_id)[:3]
    # user 추천 영양제
    recommendation_products = RecommendationProduct.objects.filter(recommendation_id = recommendations_info.recommendation_id)
    recommendation_products = get_object_or_404(recommendation_products)
    products = Product.objects.filter(product_id = recommendation_products.product_id.product_id)[:3] 
 
    # user 좋아요 영양제
    product_like_user = ProductLike.objects.filter(custom_user_id=user_id).order_by('-created_at').get()    
    product_likes = Product.objects.filter(product_id = product_like_user.product_id.product_id)[:5] 
    
    
    
    context = {'user': user, 'recommendations_info':recommendations_info,
               'ingredients':ingredients, 'survey_functions': survey_functions, 
               'products':products, 'product_likes' : product_likes                               
                  }
    
    return render(request, 'groups/main.html', context)

def group_detail(request, user_id):
    user = get_object_or_404(User, custom_user_id=user_id)
    recommendations_info = Recommendation.objects.filter(custom_user_id=user_id).order_by('-created_at')
    recommendations_info = get_object_or_404(recommendations_info)

    # user 추천 영양제
    recommendation_products = RecommendationProduct.objects.filter(recommendation_id = recommendations_info.recommendation_id)
    recommendation_products = get_object_or_404(recommendation_products)
    products = Product.objects.filter(product_id = recommendation_products.product_id.product_id)[:5] 
    context = {'user': user, 'recommendations_info':recommendations_info, 'products':products,
    }
    return render(request, 'groups/detail.html', context)

def group_individual(request, user_id, ingredient_id):
    user = get_object_or_404(User, custom_user_id=user_id)
    ingredient = Ingredient.objects.filter(ingredient_id=ingredient_id)
    product_ingredient = ProductIngredient.objects.filter(ingredient_id=ingredient_id).get()
    # user 추천 영양제
    products = Product.objects.filter(product_id = product_ingredient.product_id.product_id)[:5] 
    context = {'user': user, 'ingredient':ingredient, 'products':products,
    }
    return render(request, 'groups/individual.html', context)