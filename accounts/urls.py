from . import views
from django.urls import path

urlpatterns = [
    
    path('signup/',views.userSignUp,name='signup'),
    path('login/',views.userLogin,name='login'),

]
