import uuid
from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  

    def __str__(self):
        return self.title

class Movie(models.Model):
    collection = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255)  
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  

    def __str__(self):
        return self.title
