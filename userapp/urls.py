from . import views
from django.urls import path

urlpatterns = [
    # path('verify_token/',views.verify_token,name='verify_token'),
    path('user_profile/<int:id>',views.user_profile,name='user_profile'),
    path('userProfilePic/<int:user_id>',views.userProfilePic,name='userProfilePic'),
    path('userCoverPic/<int:user_id>',views.userCoverPic,name='userCoverPic'),
    path('profile_update/',views.user_profile_update,name='profile_update'),
    path('addaddress/',views.add_address,name='addaddress'),
    path('addressdetails/',views.address_details,name='addressdetails'),
    path('deleteaddress/',views.delete_address,name='deleteaddress'),

    path('event_details/',views.event_details,name='event_details'),
    path('booking_event/',views.booking_event,name='booking_event'),
    path('userbookedevents/<int:id>',views.bookedevent_list,name='userbookedevents'),

    path('orderlist/',views.order_list,name='orderlist'),
    path('ordercancel/',views.ordercancel,name='ordercancel'),
    path('artistpostlist/',views.artists_postlist,name='artistpostlist'),
    path('buypost/',views.buy_post,name='buypost'),
    path('checkout/',views.checkout,name='checkout'),
    
]