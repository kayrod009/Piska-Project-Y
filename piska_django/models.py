from django.db import models

class Patient(models.Model):
    username = models.CharField(max_length=300)
    password = models.IntegerField()
    email = models.EmailField(max_length=264)
