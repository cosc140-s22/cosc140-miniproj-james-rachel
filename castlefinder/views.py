from django.shortcuts import render
import requests
from .models import Castle, CastleImage
import math
import geopy.distance

apiKey = "AIzaSyCleZUFiK59QoeslAo84FCrxqwWMf1SOCM" #don't ever do this LOL

def index(request):
    addressOne = input("Address One? ")
    response = requests.get("https://nominatim.openstreetmap.org/search?format=json&q=" + addressOne)
    if response:
        if response.status_code == 200:
            result = response.json() #get the long and latitude of location input
            location = str(result[0]["lat"]) + "," + str(result[0]["lon"])
            fetchCastles(location,50000,"tourist_attraction", "castle") #call the api with these values
        else:
            print(response.status_code)
            return
    else:
        print("Connection error?")
        return
    return render(request, 'castles/index.html')


def fetchCastles(location, radius, type, keyword):
    #this function makes a request to the Google places api and should return relevant data about castles!
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ str(location) +"&radius="+ str(radius) + "&type="+ str(type) + "&keyword="+keyword+"&key=" + apiKey
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    dict = response.json()
    coordsLst = location.split(',')
    coordsOriginal = (float(coordsLst[0]), float(coordsLst[1]))
    for castle in dict["results"]:
        coordsCastle = (castle["geometry"]["location"]["lat"], castle["geometry"]["location"]["lng"])
        distance = round(geopy.dcardifistance.geodesic(coordsOriginal, coordsCastle).km, 2)
        photoReference = castle["photos"][0]["photo_reference"]
        Castle.objects.create(name = castle["name"], rating = float(castle["rating"]), distance = float(distance))
        fetchPhoto(photoReference)

        

def fetchPhoto(photoReference):
    url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=" + photoReference + "&key="+ apiKey
    payload={}
    headers = {}
    image = requests.request("GET", url, headers=headers, data=payload)
