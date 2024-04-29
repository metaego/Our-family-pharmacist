from django.shortcuts import render, redirect, get_object_or_404
from users.models import Recommendation, RecommendationIngredient, RecommendationProduct, Ingredient, SurveyFunction

# Create your views here.
def group_main(request, user_id):

    return render(request, 'group/main.html')

def group_detail(request):
    return render(request, 'group/detail.html')