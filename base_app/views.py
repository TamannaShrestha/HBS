import requests
from django.http import HttpRequest
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from base_app.models import Booking, Hotel, AppUser,Transaction
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
    hotel = get_object_or_404(Hotel, reference_id=uuid)
    
    if request.method == "POST":
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        check_in_date = request.POST.get('check_in')
        check_out_date = request.POST.get('check_out')
        
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        
        if check_in_date and check_out_date:
            Booking.objects.create(
                user=request.user,
                hotel=hotel,
                booked_on=check_in_date,
                checked_out_on=check_out_date
            )
            return redirect(reverse_lazy('payment'))
        else:
            # Handle cases where check_in_date or check_out_date is not provided
            # You can add a message to the user if necessary
            return redirect(reverse_lazy('details', kwargs={'uuid': uuid}))

    return render(request, 'base_app/details.html', {'hotel': hotel})


def login_view(request: HttpRequest) :
    if request.method == "POST" : 
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username , password=password)
        if user : 
            login(request, user)
    
    return redirect(reverse_lazy('hotels_list'))
    
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
def book_now(request,id):
    hotel=Hotel.objects.filter(id=id)
    return render(request,"base_app/checkout.html",{
        'hotel':hotel
    })
def handlesearch(request):
    query=''
    if request.method=="GET":
        query=request.GET['query']
        print(query)
        all_hotels_title = Hotel.objects.filter(name__icontains=query)
        all_hotels_content = Hotel.objects.filter(description__icontains=query)
        all_hotels = all_hotels_title.union(all_hotels_content)
        print( all_hotels_title)
    return render (request,"base_app/search.html",{
        'hotel_list':all_hotels
    })
    
    
    
def handle_payment(request):
    return render(request,'base_app/payment.html')

