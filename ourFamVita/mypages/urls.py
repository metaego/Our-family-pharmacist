from django.urls import path
from . import views

app_name = 'mypages'

urlpatterns = [
    path('<int:profile_id>/', views.mypage_main, name='mypage_main'),
    path('<int:profile_id>/views/', views.mypage_views, name='mypage_views'),
    path('<int:profile_id>/recommends/', views.mypage_recommends, name='mypage_recommends'), 
    path('<int:profile_id>/likes/', views.mypage_likes, name='mypage_likes'), 
    path('<int:profile_id>/reviews/', views.mypage_reviews, name='mypage_reviews'),  
    ]