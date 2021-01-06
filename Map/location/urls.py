from django.urls import  path
from .views import *

app_name = 'location'

urlpatterns = [
    path('location',distance_view,name = 'distance_view'),
    path('signup',signup_view,name = 'signup_view'),
    path('',login_view,name = 'login_view'),
    path('logout',logout_view,name = 'logout_view'),
    path('search',search_view,name = 'search_view'),
]