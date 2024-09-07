from django.contrib import admin

from .models import AppUser, Hotel, Review, Booking

@admin.register(AppUser)
class AppUserModelView(admin.ModelAdmin):
    list_display = ['user_id','username','is_enterprise']

@admin.register(Hotel)
class HotelModelView(admin.ModelAdmin):
    list_display = ['reference_id','name','location','is_full']

@admin.register(Review)
class ReviewModelView(admin.ModelAdmin):
    list_display = ['reference_id', 'user_id', 'hotel_id', 'rating']

@admin.register(Booking)
class BookingModelView(admin.ModelAdmin):
    list_display = ['reference_id', 'user_id', 'hotel_id', 'booked_on']