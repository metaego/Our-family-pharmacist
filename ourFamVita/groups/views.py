from django.shortcuts import render, redirect, get_object_or_404
from users.models import Recommendation, RecommendationIngredient, RecommendationProduct, Ingredient, SurveyFunction

# Create your views here.
def group_main(request, user_id):
    # recommendations_info = Recommendation.objects.filter(user_id=user_id).order_by('-created_at')
    # recommendation_ingredients = RecommendationIngredient.objects.filter(recommendations_info_id__in = recommendations.values('recommendation_id'))
    # recommendation_products = RecommendationProduct.objects.filter(recommendations_info_id__in = recommendations.values('recommendation_id'))  
    # ingredients = Ingredient.objects.filter(ingredient_id__in=recommendation_ingredients.values('ingredient_id'))
    # survey_functions = SurveyFunction.objects.filter(survey_id__in = recommendations_info.value('survey_id'))
    # return render(request, 'group/main.html', {'recommendations':recommendations, 'recommendation_products':recommendation_products, 'ingredients':ingredients,
    #                                                     'survey_functions': survey_functions,                                                                            
    #               })
    return render(request, 'group/main.html')

def group_detail(request):
    return render(request, 'group/detail.html')