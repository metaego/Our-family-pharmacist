from django.shortcuts import render, redirect, get_object_or_404
from ourFamVita.models import Profile, ProductLog, RecommendationProduct




# Create your views here.

def mypage_main(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    return render(request, 'mypages/main.html', {'profile':profile,
                                                 
                  })

def mypage_views(request, pk):
    productlog = get_object_or_404(ProductLog, profile=pk)   
    recommends = get_object_or_404(RecommendationProduct, recommendation_product_id = pk) 
    return render(request, 'mypages/views.html', {'productlog':productlog,                                                 
                  })


def mypage_recommends(request):
    pass

def mypage_likes(request):
    pass

def mypage_reviews(request):
    pass