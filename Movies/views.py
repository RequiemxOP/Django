from django.shortcuts import get_object_or_404
from django.shortcuts import render
import os
import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Task 2
from django.contrib.auth.models import User  
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .models import Collection
from .serializers import CollectionSerializer
from rest_framework import serializers

# Task 3
from django.http import JsonResponse
from django.views import View
from .middleware import RequestCounterMiddleware

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        access_token = AccessToken.for_user(user)
        return Response({'access_token': str(access_token)}, status=status.HTTP_201_CREATED)


# Collection List and Create View
class CollectionListCreateView(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        collections = self.get_queryset()
        serializer = self.get_serializer(collections, many=True)
        return Response({'collections': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = serializer.save(user=self.request.user)
        return Response({'collection_uuid': str(collection.uuid)}, status=status.HTTP_201_CREATED)


# Collection Detail View with UUID lookup
class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uuid'  

    def get_object(self):
        
        return get_object_or_404(Collection, uuid=self.kwargs['collection_uuid'])


# Fetch credentials from environment variables
API_USERNAME = os.getenv('API_USERNAME')
API_PASSWORD = os.getenv('API_PASSWORD')
API_URL = "https://demo.credy.in/api/v1/maya/movies/"

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

def get_movies(request):
    try:
        response = http.get(API_URL, auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD), timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Failed to fetch movies'}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

# Task 3
class RequestCountView(View):
    def get(self, request):
        count = RequestCounterMiddleware.get_request_count()
        return JsonResponse({"requests": count})

class ResetRequestCountView(View):
    def post(self, request):
        RequestCounterMiddleware.reset_request_count()
        return JsonResponse({"message": "request count reset successfully"})
