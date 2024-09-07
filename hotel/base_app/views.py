from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from base_app.models import Booking, Hotel, AppUser
from. import recommendation


def hotels_list_view(request: HttpRequest):
   
    ## Search Function
    query = request.GET.get('query')
    if query: 
        if len(query) > 78 : 
            all_hotels= Hotel.objects.none()
        else:
            all_hotels_title = Hotel.objects.filter(name__icontains=query)
            all_hotels_content = Hotel.objects.filter(description__icontains=query)
            all_hotels = all_hotels_title.union(all_hotels_content)
            # all_hotels = (all_hotels_content | all_hotels_title).distinct() # This works too 

        if all_hotels.count() == 0 :
            # messages.warning(request, "No search results found")
            pass
        hotel_queryset = all_hotels
    
    most_popular_id, most_id_user = recommendation.user_data(request)
    recom_hotels = Hotel.objects.filter(reference_id__in = most_popular_id)
    hotel_queryset = Hotel.objects.exclude(reference_id__in = most_popular_id)

    
    return render(request, 'base_app/hotels_list.html' , {
        'recommended_hotels' : recom_hotels,
        'hotels' : hotel_queryset,
        'query': query
    })

def detail_view(request: HttpRequest, uuid):
    context = {}
    if request.method == "POST":
        check_in_date = request.POST.get('check_in')
        check_out_date = request.POST.get('check_out')
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('hotels_list'))

        Booking(user=request.user, hotel=Hotel.objects.get(reference_id=uuid), booked_on=check_in_date, checked_out_on=check_out_date).save()
        return redirect(reverse_lazy('hotels_list'))
    
    elif request.method == "GET":
        hotel = Hotel.objects.get(reference_id=uuid)
        if not hotel:
            return redirect(reverse_lazy('hotels_list'))

        context = {
            'hotel' : hotel,
        }
    return render(request, 'base_app/details.html', context)

def login_view(request: HttpRequest) :
    if request.method == "POST" : 
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username , password=password)
        if user is not None: 
            login(request, user)
            return redirect('hotels_list')
            
    
   
    
def logout_view(request: HttpRequest) :
    if request.method == "GET" :
        if request.user.is_authenticated : 
            logout(request)
    
    return redirect(reverse_lazy('hotels_list'))

def register_view(request: HttpRequest) :

    if request.method == "POST" : 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        # Check for existing email
        if AppUser.objects.filter(email=email).exists() : 
            return redirect(reverse_lazy('hotels_list'))
        
        # Register the user
        AppUser.objects.create_user(username=first_name, first_name=first_name, last_name=last_name, email=email, password=password)
        return redirect(reverse_lazy('hotels_list'))
        
    
    return render(request, 'base_app/register.html')

def bookings_view(request: HttpRequest):
    booking_queryset = Booking.objects.filter(user=request.user)
    return render(request, "base_app/mybookings.html", {
        "bookings" : booking_queryset,
     })