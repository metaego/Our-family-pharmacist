from django.shortcuts import render, redirect, get_object_or_404
from ourFamVita.models import Profile, ProductLog, RecommendationProduct


# Create your views here.

def mypage_main(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)

    return render(request, 'mypages/main.html', {'profile': profile,
                                                 
                  })

def mypage_views(request, profile_id):
    productlog = get_object_or_404(ProductLog, profile=profile_id)   
    # recommends = get_object_or_404(RecommendationProduct, recommendation_product_id = profile_id) 
    return render(request, 'mypages/views.html', {'productlog':productlog,                                                 
                  })


def mypage_recommends(request):
    pass

def mypage_likes(request):
    pass

def mypage_reviews(request):
    pass