from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # /home/{profile-id}/surveys/{survey-id}
    path('profile_main/<profile_id>', views.home_main, name='home_main'),
]
