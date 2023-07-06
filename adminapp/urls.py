from django.urls import path
from adminapp import views
from adminapp.views import *

urlpatterns = [
    path('adminlogin/',views.adminLogin.as_view(),name='adminlogin'),
    path('adminlogout/',views.Admin_Logout,name='adminlogout'),
    path('userlist/',views.UserList.as_view(),name='userlist'),
    path('artistlist/',views.artist_list,name='artistlist'),
    path('postlist/',views.post_list,name='postlist'),
    path('admineventlist/',views.event_list,name='admineventlist'),
    path('orderlist/',views.order_list,name='orderlist'),

    path('admindeletepost/<int:id>/',views.delete_post,name='admindeletepost'),
    path('eventdelete/',views.delete_event,name='eventdelete'),
    path('postdelete/',views.delete_post,name='postdelete'),
    path('blockuser/<int:user_id>/',views.block_user,name='blockuser'),
    path('blockartist/<int:artist_id>/',views.block_artist,name='blockartist'),
]