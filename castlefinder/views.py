from django.shortcuts import render, get_object_or_404
import requests
from .models import Castle, DropDown
import math
import os
from django.db.models import Prefetch
import geopy.distance
from django.core.files import File
from .forms import CastleFilterForm, DropDownForm

apiKey = "AIzaSyCleZUFiK59QoeslAo84FCrxqwWMf1SOCM" #don't ever do this LOL
foundCastles = []

def index(request):
    model = DropDown()
    form_class = DropDownForm()
    template_name = 'myapp/template.html'
    success_url = 'myapp/success.html'

    form = CastleFilterForm(request.GET)
    loc_search = request.GET.get('location_search')
    if request.GET.get('history'):
        loc_search = request.session["previousLoc"]
    if loc_search:
        response = requests.get("https://nominatim.openstreetmap.org/search?format=json&q=" + loc_search)
        if response:
            if response.status_code == 200:
                result = response.json() #get the long and latitude of location input
                location = str(result[0]["lat"]) + "," + str(result[0]["lon"])
                request.session["previousLoc"] = loc_search
                foundCastles = fetchCastles(location,50000,"tourist_attraction", "castle") #call the api with these values
            else:
                print(response.status_code)
                return
        else:
            print("Connection error?")
            return
        
        #filter the table categories
       
        name = request.GET.get('name')
        if name:
            products = Castle.objects.all().order_by('name')
        distance = request.GET.get('distance')
        if distance:
            products = Castle.objects.all().order_by('distance')
        rating = request.GET.get('rating')
        if rating:
            products = Castle.objects.all().order_by('rating')


        context = {"castles": foundCastles, 'form': form}
        return render(request, 'castles/index.html', context=context)
    else:
        context = {"castles": None, 'form': form}
        return render(request, 'castles/index.html', context=context)

        
    
    
    


def fetchCastles(location, radius, type, keyword):
    #this function makes a request to the Google places api and should return relevant data about castles!
    foundCastles = []
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ str(location) +"&radius="+ str(radius) + "&type="+ str(type) + "&keyword="+keyword+"&key=" + apiKey
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    dict = response.json()
    coordsLst = location.split(',')
    coordsOriginal = (float(coordsLst[0]), float(coordsLst[1]))
    for castle in dict["results"]:
        coordsCastle = (castle["geometry"]["location"]["lat"], castle["geometry"]["location"]["lng"])
        distance = round(geopy.distance.geodesic(coordsOriginal, coordsCastle).km, 2)
        photoReference = castle["photos"][0]["photo_reference"]
        imageReference = url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=" + photoReference + "&key="+ apiKey
        if not Castle.objects.filter(name =castle["name"] ).exists():
            currentCastle = Castle.objects.create(name = castle["name"], rating = float(castle["rating"]), distance = float(distance), imageReference = imageReference)
        else: 
            currentCastle = Castle.objects.filter(name =castle["name"])[0]
        foundCastles.append(currentCastle)
    return foundCastles
        
'''
def fetchPhoto(photoReference, currentcastle):
    url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=" + photoReference + "&key="+ apiKey
    payload={}
    headers = {}
    image = requests.request("GET", url, headers=headers, data=payload)
    with open(photoReference + '.jpg', 'wb') as f: #workaround 
        f.write(image.content)
    reopen = open(photoReference + '.jpg', 'rb')
    django_file = File(reopen)
    CastleImage.objects.create(image = django_file, castle = currentcastle)
    os.remove(photoReference + '.jpg')'''


def show(request, castle_id):
    c = get_object_or_404(Castle, pk=castle_id)
    context = { 'castle': c }
    return render(request, 'castles/show.html', context)




