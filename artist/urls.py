from . import views
from django.urls import path

urlpatterns = [
    path('artistsignup/',views.artistSignUp.as_view(),name='artistsignup'),
    path('artist_login/',views.artist_Login,name='artist_login'),
    path('artistgooglelogin/',views.google_artistLogin,name='artistgooglelogin'),
    path('artist_profile/<int:id>',views.artist_profile,name='artist_profile'),
    path('addProfilePic/<int:artist_id>',views.addProfilePic,name='addProfilePic'),
    path('addCoverPic/<int:artist_id>',views.addCoverPic,name='addCoverPic'),
    path('profile_update/<int:id>',views.artist_profile_update,name='profile_update'),
    path('addartistaddress/',views.add_artistaddress,name='addartistaddress'),
    path('getartistaddress/<int:artistid>',views.get_address,name='getartistaddress'),

    path('artistpostlist/<int:artist_id>',views.artistpost_list,name='artistpostlist'),
    path('artisteventlist/<int:artist_id>',views.artistevent_list,name='artisteventlist'),

    path('createpost/',views.create_posts,name='createpost'),
    path('postlist/',views.post_list,name='postlist'),
    path('editpost/<int:postid>',views.edit_post,name='editpost'),
    path('deletepost/<int:id>',views.delete_post,name='deletepost'),

    path('addevent/',views.add_event,name='addevent'),
    path('eventlist/',views.event_list,name='eventlist'),
    path('editevent/<int:id>',views.edit_event,name='editevent'),
    path('deleteevent/<int:id>',views.delete_event,name='deleteevent'),

    path('bookevent/',views.book_event,name='bookevent'),
    path('userbookedevents/<int:id>',views.bookedevent_userlist,name='userbookedevents'),
    path('artistbookedevents/<int:id>',views.bookedevent_artistlist,name='artistbookedevents'),

    path('orderpost/',views.order_post,name='orderpost'),
    path('getorders/<int:artist_id>',views.get_orders,name='getorders'),
    path('viewartistorders/<int:artist_id>',views.view_artistorders,name='viewartistorders'),
    path('editorderstatus/<int:order_id>',views.editorder_status,name='editorderstatus'),
    path('orderdetails/',views.order_details,name='orderdetails'),
]