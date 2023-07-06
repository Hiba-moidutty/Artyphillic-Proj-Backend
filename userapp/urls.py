from . import views
from django.urls import path

urlpatterns = [
    path('verify_token/',views.verify_token,name='verify_token'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('profile_update/',views.user_profile_update,name='profile_update'),
    path('addaddress/',views.add_address,name='addaddress'),
    path('addressdetails/',views.address_details,name='addressdetails'),
    path('deleteaddress/',views.delete_address,name='deleteaddress'),

    path('event_details/',views.event_details,name='event_details'),
    path('booking_event/',views.booking_event,name='booking_event'),
    path('bookedevents/',views.bookedevent_list,name='bookedevents'),

    path('orderlist/',views.order_list,name='orderlist'),
    path('ordercancel/',views.ordercancel,name='ordercancel'),
    path('artistpostlist/',views.artists_postlist,name='artistpostlist'),
    path('buypost/',views.buy_post,name='buypost'),
    path('checkout/',views.checkout,name='checkout'),
    
]