from django.shortcuts import render,redirect
from .models import *
from .forms import *
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

# Create your views here.

# noinspection PyProtectedMember
def distance_view(request):
    username = None
    location = None
    destination = None
    distance = None
    form = locationModelForm()
    geolocator = Nominatim(user_agent=('location'))
    m = folium.Map(width=800, height=500)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('location:login_view')
    if request.method == 'POST':
        g = locationModelForm(request.POST)
        if g.is_valid():
            # location coordinates

            location_ = g.cleaned_data.get('location')
            location = geolocator.geocode(location_)
            print(location)
            l_lat = location.latitude
            l_long = location.longitude
            print(l_lat,l_long)
            pointA = (l_lat,l_long)

            # destination coordinates

            destination_ = g.cleaned_data.get('destination')
            destination = geolocator.geocode(destination_)
            print(destination)
            d_lat = destination.latitude
            d_long = destination.longitude
            print(d_lat,d_long)
            pointB = (d_lat,d_long)

            # caculate distance

            distance = round(geodesic(pointA,pointB).km,2)
            print(distance)
            if distance > 1000:
                zoom = 1
            if distance > 100:
                zoom = 6
            if distance < 100:
                zoom = 10
            pointC =((l_lat+d_lat)/2,(l_long+d_long)/2)
            m = folium.Map(width=800, height=500, location=pointC, zoom_start=zoom)
            folium.Marker([l_lat, l_long], popup=location,
                          icon=folium.Icon(color='red', icon='male', prefix='fa')).add_to(m)
            folium.Marker([d_lat, d_long], popup=destination,
                          icon=folium.Icon(color='red', icon='male', prefix='fa')).add_to(m)
            line = folium.PolyLine(locations=[pointA,pointB],weight = 1,color = 'blue')
            m.add_child(line)

    m = m._repr_html_()

    context = {
        'username':username,
        'distance' : distance,
        'location':location,
        'destination':destination,
        'form':form,
        'map' : m,
    }
    return render(request,'location/caculate.html',context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Sign Up completed')
        else:
            messages.error(request,'Sign Up Failed')
    form = UserCreationForm()
    return render(request,'location/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(request,username = username,password = password)
        if account is None:
            form = AuthenticationForm()
            messages.error(request,'The user name or password is incorrect')
            return render(request, 'location/login.html', {'form': form})
        else:
            login(request,account)
            return redirect('location:distance_view')
    else :
        form = AuthenticationForm()
        return render(request,'location/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('location:login_view')

def search_view(request):
    form = placeModelForm()
    geolocator = Nominatim(user_agent=('location'))
    m = folium.Map(location=[21.005879541619166, 105.84731970239473],width=800, height=500,zoom_start=14)
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    else :
        return redirect('location:login_view')
    if request.method == 'POST':
        g = placeModelForm(request.POST)
        if g.is_valid():
            location_ = g.cleaned_data.get('name')
            location = geolocator.geocode(location_)
            print(location)
            l_lat = location.latitude
            l_long = location.longitude
            print(l_lat,l_long)
            pointA = (l_lat,l_long)
            m = folium.Map(width=800, height=500, location=pointA, zoom_start=24)
            folium.Marker([l_lat, l_long], popup=location,
                          icon=folium.Icon(color='red', icon='male', prefix='fa')).add_to(m)
    else:
        lst = place.objects.all()
        for obj in lst:
            if obj.type == 'restaurant':
                folium.Marker([obj.lat, obj.long], popup=obj.name,
                              icon=folium.Icon(color='red', icon='building-o', prefix='fa')).add_to(m)
            elif obj.type == 'bank':
                folium.Marker([obj.lat, obj.long], popup=obj.name,
                              icon=folium.Icon(color='blue', icon='usd', prefix='fa')).add_to(m)
            else :
                folium.Marker([obj.lat, obj.long], popup=obj.name,
                              icon=folium.Icon(color='green', icon='fa-graduation-cap', prefix='fa')).add_to(m)
    m = m._repr_html_()

    context = {
        'username':username,
        'form':form,
        'map' : m,
    }
    return render(request,'location/search.html',context)
