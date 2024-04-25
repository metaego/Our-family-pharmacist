from django.urls import path
from . import views

app_name = 'mypages'

urlpatterns = [
    path('<int:pk>/', views.mypage_main, name='mypage_main'),
    path('<int:pk>/views/', views.mypage_views, name='mypage_views'),
    path('<int:pk>/recommends/', views.mypage_recommends, name='mypage_recommends'), 
    path('<int:pk>/likes/', views.mypage_likes, name='mypage_likes'), 
    path('<int:pk>/reviews/', views.mypage_reviews, name='mypage_reviews'),  
    ]