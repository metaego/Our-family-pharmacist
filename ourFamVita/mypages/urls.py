from django.urls import path
from . import views

app_name = 'mypages'

urlpatterns = [
    path('<int:pk>/', views.mypage_main, name='main'),
    path('<int:pk>/views/', views.mypage_views, name='views'),
    path('<int:pk>/recommends/', views.mypage_recommends, name='recommends'), 
    path('<int:pk>/likes/', views.mypage_likes, name='likes'), 
    path('<int:pk>/reviews/', views.mypage_reviews, name='reviews'),  
    ]