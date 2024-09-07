from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import handle_payment, handlesearch, hotels_list_view, login_view, logout_view, register_view, detail_view, bookings_view,book_now

urlpatterns = [
    path('', hotels_list_view , name='hotels_list'),
    path('login/', login_view , name='login'),
    path('logout/', logout_view , name='logout'),
    path('register/', register_view , name='register'),
    path('details/<str:uuid>', detail_view, name='details'),
    path('bookings/',bookings_view, name="bookings"),
    path('book_now/<int:id>/',book_now,name="book_now"),
    path('payment/',handle_payment,name="payment"),
    path('search/',handlesearch,name="search")
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)