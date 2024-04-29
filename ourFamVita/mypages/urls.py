from django.urls import path
from . import views

app_name = 'mypages'

urlpatterns = [
    path('<int:profile_id>/', views.mypage_main, name='main'),
    path('<int:profile_id>/views/', views.mypage_views, name='views'),
    path('<int:profile_id>/recommends/', views.mypage_recommends, name='recommends'), 
    path('<int:profile_id>/likes/', views.mypage_likes, name='likes'), 
    path('<int:profile_id>/reviews/', views.mypage_reviews, name='reviews'),  
    ]