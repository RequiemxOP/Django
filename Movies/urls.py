from django.urls import path
from .views import get_movies

# Task 2
from .views import UserRegistrationView, CollectionListCreateView, CollectionDetailView

# Task 3
from .views import RequestCountView, ResetRequestCountView

urlpatterns = [
    path('movies/', get_movies, name='movie_list'), 
   
    # User Registration and Collection Endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('collection/', CollectionListCreateView.as_view(), name='collection-list-create'),
    
    # Use 'collection_uuid' instead of 'pk' to match test.py and views
    path('collection/<uuid:collection_uuid>/', CollectionDetailView.as_view(), name='collection-detail'),

    # Task 3
    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', ResetRequestCountView.as_view(), name='reset-request-count'),
]
