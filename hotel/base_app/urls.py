from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import hotels_list_view, login_view, logout_view, register_view, detail_view, bookings_view

urlpatterns = [
    path('', hotels_list_view , name='hotels_list'),
    path('login/', login_view , name='login'),
    path('logout/', logout_view , name='logout'),
    path('register/', register_view , name='register'),
    path('details/<str:uuid>', detail_view, name='details'),
    path('bookings/',bookings_view, name="bookings")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)