from django.shortcuts import render, get_object_or_404
from .models import Location

# Create your views here.
def browse(request):
    locationList = Location.objects.all()
    print(locationList)

    context = {
        "locationList": locationList
    }
    return render(request, "browse.html", context)


def productDetails(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    context ={
        "location":location
    }
    return render(request, "details.html", context=context)

