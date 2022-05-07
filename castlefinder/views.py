from django.shortcuts import render
import requests
import math

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
    print(response.text)
