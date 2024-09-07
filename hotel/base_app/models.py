import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


class AppUser(AbstractUser):
    user_id = models.CharField(max_length=36, primary_key=True, unique=True, default=uuid.uuid4)
    is_enterprise = models.BooleanField(default=False)

class BaseClass(models.Model): 
    is_deleted = models.BooleanField(default=False)
    reference_id = models.CharField(max_length=36, primary_key=True, unique=True, default=uuid.uuid4)

    class Meta:
        abstract = True

class Hotel(BaseClass):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    is_full = models.BooleanField()
    description = models.TextField(max_length=1000, blank=True)
    rating = models.IntegerField(blank=True,null=True, validators=[MinValueValidator(1),MaxValueValidator(5)])
    description_image = models.ImageField(upload_to='uploads/' , blank=True)

    @property
    def get_average_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        self.rating = round(avg_rating) if avg_rating else 0.00
        self.save()
        return round(avg_rating,1) if avg_rating else 0.00
    

class Review(BaseClass):
    user = models.ForeignKey(AppUser, on_delete=models.PROTECT, related_name="+")
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

class Booking(BaseClass):
    user = models.ForeignKey(AppUser, on_delete=models.PROTECT, related_name="+")
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name="bookings")
    booked_on = models.DateField()
    checked_out_on = models.DateField()