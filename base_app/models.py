import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.contrib.auth.models import User

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
    
    
class Order(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.PROTECT, related_name="+")
    price = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=100,default="pokhara")
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.user.user_id
    
class Transaction(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_id=models.CharField(max_length=200,null=True)
    amount=models.CharField(max_length=200)
    user=models.CharField(max_length=200)
    created_date=models.DateField(auto_now=True)
    
    
    