from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile, ProductLog, Product, Recommendation, RecommendationIngredient, Ingredient, SurveyFunction, ProductLike, ProductReview


# Create your views here.

def mypage_main(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)
    context = {'profile': profile,
                  }
    return render(request, 'mypages/main.html', context)



def mypage_views(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)
    productlogs = ProductLog.objects.filter(profile_id=profile_id).order_by('-leaved_at')
    products = Product.objects.all()[:5] 
    context =  {'profile': profile,'productlogs': productlogs, 'products': products,
                }
    return render(request, 'mypages/views.html', context)



def mypage_recommends(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)     
    recommendations_info = Recommendation.objects.filter(profile_id=profile_id).order_by('-created_at')
    recommendations_info = get_object_or_404(recommendations_info)
    recommendation_ingredients = RecommendationIngredient.objects.filter(recommendation_id = recommendations_info.recommendation_id)
    recommendation_ingredients = get_object_or_404(recommendation_ingredients)
    ingredients = Ingredient.objects.filter(ingredient_id = recommendation_ingredients.ingredient_id.ingredient_id)[:5] 
    survey_functions = SurveyFunction.objects.filter(survey_id = recommendations_info.survey_id).get()
    context = {'profile': profile, 'recommendations_info':recommendations_info, 'recommendation_ingredients':recommendation_ingredients, 
               'ingredients':ingredients, 'survey_functions': survey_functions,                                  
                  }
    return render(request, 'mypages/recommends.html', context)


def mypage_likes(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id) 
    product_like = ProductLike.objects.filter(profile_id=profile_id).order_by('-created_at').get()    
    products = Product.objects.filter(product_id = product_like.product_id.product_id)[:5] 
    context = {'profile': profile, 'products':products,                                 
                  }
    return render(request, 'mypages/likes.html', context)    
     

def mypage_reviews(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id) 
    product_reviews = ProductReview.objects.filter(profile_id=profile_id).order_by('-created_at')
    product_reviews= get_object_or_404( product_reviews)
    products = Product.objects.filter(product_id = product_reviews.product_id.product_id)[:5] 
    context = {'profile': profile, 'products':products, 'product_reviews':product_reviews,                                   
                  }
    return render(request, 'mypages/reviews.html', context)    

