from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('rec-nut-products/<int:user_id>/', views.group_main, name='group_main'),
    path('rec-total-products/<int:user_id>/', views.group_detail, name='group_detail'),
    path('rec-nut-products/<int:user_id>/<int:ingredient_id>/', views.group_individual, name='group_individual'), 
    
    ]