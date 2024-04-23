from django.urls import path
from profiles.views import profile, survey1, survey2, survey3, profile_info, profile_delete

urlpatterns = [
    path("", profile),
    path("survey-1/", survey1),
    path("survey-2/", survey2),
    path("survey-3/", survey3),
    path("profile-id/profile-info/", profile_info),
    path("profile-id/", profile_delete),
    
]
