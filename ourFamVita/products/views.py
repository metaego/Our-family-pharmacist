from django.shortcuts import render, redirect
from django.utils import timezone
from users.models import (Product, ProductReview, Profile
                          , ProductReview, ProductIngredient, Ingredient)

# Create your views here.
def product_detail(request, product_id, profile_id):
    # AI추천받기:영양제 상세보기
    # menu: 영양제 추천받기 > 영양 성분 리포트 > 영양제 추천 목록 > 영양제 상세보기
    # /products/{product-id}/{profile-id}
    profile = Profile.objects.get(profile_id=profile_id)
    product = Product.objects.get(pk=product_id)

    product_ingredients = ProductIngredient.objects.filter(product_id=product_id).values_list('ingredient_id', flat=True)
    product_ingredients = list(product_ingredients)
    product_ingredients = Ingredient.objects.filter(ingredient_id__in=product_ingredients)
    review = ProductReview.objects.filter(product_id=product_id, profile_id=profile_id).exists()
    if review:
        review = ProductReview.objects.filter(product_id=product_id, profile_id=profile_id).get()
    print(f'review: {review}')

    return render(request, 'products/product_detail.html', {
        'product': product, 
        'review':review,
        'profile': profile,
        'product_ingredients': product_ingredients,
    })


def product_review(request, product_id, profile_id):
    profile = Profile.objects.get(profile_id=profile_id)
    product = Product.objects.get(product_id=product_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        ProductReview.objects.create(product_review_rating=rating,
                                     product_review_content=comment,
                                     product_id=product,
                                     created_at=timezone.now(),
                                     profile_id=profile)
    return redirect('products:products_detail', product.product_id, profile.profile_id)
# return redirect('recommends:profile_total_report', profile.profile_id, survey.survey_id)