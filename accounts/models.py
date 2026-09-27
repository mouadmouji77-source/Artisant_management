from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('artisan', 'Artisan'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
# models.py

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    demand = models.IntegerField(default=0)  # Set a default value for demand
    contact_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title

    def get_artisan_name(self):
        return self.artisan.get_full_name() if self.artisan else 'Unknown Artisan'

    def average_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else None


class Demand(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    )
    
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='demands')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    requested_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.username} - {self.service.title} ({self.status})"

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.service} by {self.client}"

class ServiceStatus(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.client.username} - {self.service.title} ({self.status})"
