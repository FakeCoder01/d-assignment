from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from core.api.hackathon import HackathonViewSet
from core.api.submission import SubmissionViewSet
from . import views
urlpatterns = [
    path('auth/token/', ObtainAuthToken.as_view(), name='api_token_auth'),
    path('hackathon/', HackathonViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='api_hackathon'), 

    path('hackathon/<str:id>/', HackathonViewSet.as_view({
        'get': 'retrieve',
        'update': 'update',
        'put': 'update',
        'delete': 'destroy',
    }), name='api_hackathon_details'),

    path('submission/', SubmissionViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='api_submission'),

    path('submission/<str:id>/', HackathonViewSet.as_view({
        'get': 'retrieve',
        'update': 'update',
        'delete': 'destroy',
    }), name='api_submission_details'),

    path('hackathon/<str:id>/submissions/', HackathonViewSet.as_view({
        'get': 'all_submissions',
    }), name='api_hackathon_submission_details'),

    path('hackathons/', views.get_all_hackathons, name="get_all_hackathons"),
    path('hackathons/<str:id>/', views.get_hackathon, name="get_hackathon"),
    
]
