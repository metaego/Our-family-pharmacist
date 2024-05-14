from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile, ProductLog, Product, Recommendation, RecommendationIngredient, Ingredient, SurveyFunction, ProductLike, ProductReview, FunctionCode


# Create your views here.

def mypage_main(request, profile_id):

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    profile = get_object_or_404(Profile, profile_id=profile_id)
    context = {'profile': profile,
                  }
    return render(request, 'mypages/main.html', context)



def mypage_views(request, profile_id):

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    profile = get_object_or_404(Profile, profile_id=profile_id)
    productlogs = ProductLog.objects.filter(profile_id=profile_id).order_by('-visited_at')
    products = Product.objects.all()[:5] 
    context =  {'profile': profile,'productlogs': productlogs, 'products': products,
                }
    return render(request, 'mypages/views.html', context)


def mypage_recommends(request, profile_id):

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    profile = get_object_or_404(Profile, profile_id=profile_id)     
    recommendations_info = Recommendation.objects.filter(profile_id=profile_id).order_by('-created_at')[:5]
    ingredients_list = []

    for recommendation in recommendations_info: 
        ingredients_info = []
        functions_info = []
        recommendation_ingredients = RecommendationIngredient.objects.filter(recommendation_id=recommendation.recommendation_id)
        
        for recommendation_ingredient in recommendation_ingredients:
            ingredients = Ingredient.objects.get(ingredient_id=recommendation_ingredient.ingredient_id.ingredient_id)
            ingredients_info.append(ingredients)

        survey_functions = SurveyFunction.objects.filter(survey_id=recommendation.survey_id) 

        for survey_function in survey_functions:
            function_codes = FunctionCode.objects.get(function_code = survey_function.function_code.function_code)
            functions_info.append(function_codes)
            
        info = [ingredients_info, functions_info, recommendation]
        ingredients_list.append(info)

    context = {
        'profile': profile,
        'ingredients_list': ingredients_list,
    }
    return render(request, 'mypages/recommends.html', context)


def mypage_likes(request, profile_id):

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    profile = get_object_or_404(Profile, profile_id=profile_id) 
    product_likes = ProductLike.objects.filter(profile_id=profile_id).order_by('-created_at')[:5]
    products_list = []
    for product_like in product_likes:
        products = Product.objects.get(product_id = product_like.product_id.product_id)
        products_list.append(products)
    
        context = {'profile': profile, 'products':products, 'products_list':products_list,                                
                  }
        return render(request, 'mypages/likes.html', context)    
     

def mypage_reviews(request, profile_id):

    user_id = request.session.get('user')
    if not user_id:
        return redirect('/')
    
    profile = get_object_or_404(Profile, profile_id=profile_id) 
    product_reviews = ProductReview.objects.filter(profile_id=profile_id).order_by('-created_at')[:5]
    products_list = []
    for product_review in product_reviews:
        products = Product.objects.get(product_id = product_review.product_id.product_id)
        products_info= [product_review, products]
        products_list.append(products_info)
    print(products_list)    
    context = {'profile': profile, 'products':products, 'product_reviews':product_reviews, 
               'products_list':products_list,                                   
                  }
    return render(request, 'mypages/reviews.html', context)    

