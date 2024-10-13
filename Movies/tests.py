from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from .models import Collection
from .serializers import CollectionSerializer
import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .middleware import RequestCounterMiddleware

class MoviesAPITestCase(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()

        # Generate a JWT token for the user
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Sample collection data
        self.collection_data = {
            "title": "My Movie Collection",
            "description": "A collection of my favorite movies.",
            "movies": [
                {
                    "title": "Inception",
                    "description": "A mind-bending thriller.",
                    "genres": "Sci-Fi, Thriller",
                    "uuid": "123e4567-e89b-12d3-a456-426614174000"
                }
            ]
        }

    # Helper method to create a collection and return its UUID
    def create_collection(self):
        response = self.client.post('/collection/', self.collection_data, format='json')
        print(f"Create collection response: {response.status_code}")
        print(f"Create collection content: {response.content}")
        self.assertEqual(response.status_code, 201, "Failed to create collection in helper method.")
        return response.data['collection_uuid']

    # Test the registration endpoint
    def test_user_registration(self):
        response = self.client.post('/register/', {"username": "newuser", "password": "newpass"}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.data)

    # Test creating a collection
    def test_create_collection(self):
        response = self.client.post('/collection/', self.collection_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('collection_uuid', response.data)

    # Test fetching collections
    def test_get_collections(self):
        self.create_collection()  
        response = self.client.get('/collection/')
        print(f"Get collections response: {response.status_code}")
        print(f"Get collections content: {response.content}")

        self.assertEqual(response.status_code, 200)
        self.assertIn('collections', response.data, f"Response data: {response.data}")
        self.assertGreater(len(response.data['collections']), 0, "No collections found")

    # Test updating a collection
    def test_update_collection(self):
        collection_uuid = self.create_collection() 
        print(f"Updating collection with UUID: {collection_uuid}")

       
        updated_data = {
            "title": "Updated Movie Collection",
            "description": "An updated description",
        }
        response = self.client.put(f'/collection/{collection_uuid}/', updated_data, format='json')
        print(f"Update collection response: {response.status_code}")
        print(f"Update collection content: {response.content}")

        self.assertEqual(response.status_code, 200, f"Update failed: {response.content}")
        self.assertEqual(response.data['title'], "Updated Movie Collection")

    # Test deleting a collection
    def test_delete_collection(self):
        collection_uuid = self.create_collection() 
        print(f"Deleting collection with UUID: {collection_uuid}")

       
        response = self.client.delete(f'/collection/{collection_uuid}/')
        print(f"Delete collection response: {response.status_code}")
        print(f"Delete collection content: {response.content}")

        self.assertEqual(response.status_code, 204, f"Delete failed: {response.content}")

        
        get_after_delete = self.client.get(f'/collection/{collection_uuid}/')
        print(f"Get after delete response: {get_after_delete.status_code}")
        print(f"Get after delete content: {get_after_delete.content}")
        self.assertEqual(get_after_delete.status_code, 404, "Collection still exists after deletion")

# Task 3
class RequestCountAPITest(APITestCase):
    def setUp(self):
        self.get_request_count_url = reverse('request-count')
        self.reset_request_count_url = reverse('reset-request-count')
        # Reset request count before each test
        self.client.post(self.reset_request_count_url)

    def test_get_request_count(self):
        # Simulate a few requests
        response = self.client.get(self.get_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['requests'], 1) 

        response = self.client.get(self.get_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['requests'], 2) 

    def test_reset_request_count(self):
        # Simulate a request to increment the counter
        response = self.client.get(self.get_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['requests'], 1)  # First request

        
        response = self.client.post(self.reset_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], "request count reset successfully")

        
        response = self.client.get(self.get_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['requests'], 1)  
