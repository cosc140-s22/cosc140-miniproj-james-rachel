from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import Castle
import math
import os
from django.db.models import Prefetch
import geopy.distance
from django.core.files import File
from .forms import CastleFilterForm, DropDown, ReviewForm
from django.contrib.auth.models import User


apiKey = "AIzaSyCleZUFiK59QoeslAo84FCrxqwWMf1SOCM" #don't ever do this LOL
foundCastles = []

def index(request):
    dropDown = DropDown()

    form = CastleFilterForm(request.GET)
    loc_search = request.GET.get('location_search')
    if request.GET.get('history'):
        loc_search = request.session["previousLoc"]
    if request.GET.get('filter') and request.session["previousLoc"] != None:
        filter = request.GET.get('filter')
        foundCastles = Castle.objects.filter(searchWord= request.session["previousLoc"]).order_by(filter)
        context = {"castles": foundCastles, 'form': form, "dropdown": dropDown}
        return render(request, 'castles/index.html', context=context)
    if loc_search:
        response = requests.get("https://nominatim.openstreetmap.org/search?format=json&q=" + loc_search)
        if response:
            if response.status_code == 200:
                result = response.json() #get the long and latitude of location input
                if len(result) == 0:
                    context = {"castles": None, 'form': form, "dropdown": dropDown} #exit because invalid location
                    return render(request, 'castles/index.html', context=context)
                location = str(result[0]["lat"]) + "," + str(result[0]["lon"])
                request.session["previousLoc"] = loc_search
                foundCastles = fetchCastles(location,50000,"tourist_attraction", "castle", loc_search) #call the api with these values
            else:
                print(response.status_code)
                return
        else:
            print("Connection error?")
            return

        context = {"castles": foundCastles, 'form': form, "dropdown": dropDown}
        return render(request, 'castles/index.html', context=context)
    else:
        #clear session key
        request.session['previousLoc'] = None
        context = {"castles": None, 'form': form, "dropdown": dropDown}
        return render(request, 'castles/index.html', context=context)

    


def fetchCastles(location, radius, type, keyword, loc_search):
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
        placeid = castle["place_id"]
        imageReference = url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=" + photoReference + "&key="+ apiKey
        if not Castle.objects.filter(name =castle["name"] ).exists():
            try:
                currentCastle = Castle.objects.create(name = castle["name"], rating = float(castle["rating"]), distance = float(distance), imageReference = imageReference, searchWord = loc_search, placeID=placeid)
            except:
                print("An exception occurred")
        else: 
            currentCastle = Castle.objects.filter(name =castle["name"])[0]
        foundCastles.append(currentCastle)
    return foundCastles

#this was too slow, but leaving it here anyway         
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
    address = fetchReviews(c.placeID, c, request) #this runs before the render so we should see the google reviews fetched
    context = { 'castle': c, 'address': address }
    return render(request, 'castles/show.html', context)
    


def fetchReviews(placeId, c, request):
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + placeId + "&key=" + apiKey
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    dict = response.json()
    address = dict["result"]["formatted_address"]
    for review in dict["result"]["reviews"]:
        authorName = review["author_name"]
        reviewText = review["text"]
        reviewRating = review["rating"]
        if c.review_set.filter(Author =authorName ).exists():
            break
        c.review_set.create(rating=reviewRating, review=reviewText, Author= authorName ) #create a review model and attatch it to this castle
    return address
        


#creating a review manually * not from google api *
def createreview(request, castle_id):
    c = get_object_or_404(Castle, pk=castle_id)
    if request.method == 'POST':
      form = ReviewForm(request.POST)
      if form.is_valid():
        c.review_set.create(Author=form.cleaned_data['Author'], rating=form.cleaned_data['rating'], review=form.cleaned_data['review'])
        return redirect('show', c.id)
    else:
      form = ReviewForm()
    context = { 'form':form, 'castle':c }
    return render(request, 'castles/review.html', context)