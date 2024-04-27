from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile, ProductLog, Product, Recommendation, RecommendationIngredient, Ingredient, SurveyFunction, ProductLike, ProductReview


# Create your views here.

def mypage_main(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'mypages/main.html', {'profile': profile,
                  })


def mypage_views(request, pk):
    productlogs = ProductLog.objects.filter(pk=pk).order_by('-leaved_at').get()
    products = Product.objects.filter(pk=productlogs.values('product_id'))

    return render(request, 'mypages/views.html', {'productlogs': productlogs, 'products': products})


def mypage_recommends(request, pk):
     
    recommendations_info = Recommendation.objects.filter(pk=pk).order_by('-created_at')
    recommendations = RecommendationIngredient.objects.filter(recommendation_info_id__in = recommendations.values('recommendation_id')) 
    ingredients = Ingredient.objects.filter(ingredient_id__in=recommendations.values('ingredient_id'))
    survey_functions = SurveyFunction.objects.filter(survey_id__in = recommendations_info.value('survey_id'))
    return render(request, 'mypages/recommends.html', {'recommendations':recommendations, 'ingredients':ingredients,
                                                        'survey_functions': survey_functions,                                       
                  })


# 밑에 가져오는 방식 확인 후 위처럼 수정할 지 결정

def mypage_likes(request, profile_id):
    product_like = ProductLike.objects.filter(profile_id=profile_id).order_by('-created_at')
    product_like = get_object_or_404(product_like)
    products = Product.objects.filter(product_id = product_like.product_id)
    products = get_object_or_404(products)
    return render(request, 'mypages/likes.html', {'products':products,                                 
                  })    
     

def mypage_reviews(request, pk):
    product_reviews = ProductReview.objects.filter(pk=pk).order_by('-created_at')
    product_reviews = get_object_or_404(product_reviews)    
    products = Product.objects.filter(product_id = product_reviews.product_id)
    products = get_object_or_404(products)
    return render(request, 'mypages/reviews.html', {'products':products, 'product_reviews':product_reviews,                                   
                  })    

