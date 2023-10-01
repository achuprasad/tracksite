from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    is_driver = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Ride(models.Model):
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

    STATUS_CHOICES = [
        (REQUESTED, 'Requested'),
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    rider = models.ForeignKey(CustomUser, related_name='rides_as_rider', on_delete=models.CASCADE)
    driver = models.ForeignKey(CustomUser, related_name='rides_as_driver', on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)



