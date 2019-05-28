from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
''' VIEWS

    Volunteer landing page
        - must be able to make a new account
        - signed in has buttons for adding new family/asylees, new travel, new sponsor
        - travel view
            - able to quickly jot information down,
            - able to confirm/check confirmation numbers,
            - links to print tickets/boarding passes,

    Asylees prepared for departure
        - base and sort this view off of their travel mode, travel time, and city van time,
        - lists by departure time minus 4 hrs for the airport and 3 hrs for the bus, 2 hrs for the train so that transport can be arranged and departure bags prepared,
        - printable forms per family for traveling,

    Administrative views:
        - current number of asylees and volunteers on site (with ratio)
        - TSA form submitted to CBP at night for asylum seekers traveling by air the next day: travel date, all names exactly as on ICE form, alien numbers, airline, flight number, flight, time of departure, first stop of the flight.

    Statistics
        - # & % by country of origin,
        - # & % by destination,
        - # & % by sex,
        - # & % by age,
        - # & % by language spoken,
        - # & % by duration between arrival and confirmation of travel,
        - # & % by duration between arrival and departure,
        - # & % by mode of travel,
        - list view sorted by time since arrival,

    Preferences
        - View filters
            - Only those still here/everyone who has passed through
            - Travel prepared?
            - Mode of Travel? (air/bus/train)
            - View for ABQ/RR
'''

def index(request):
    return HttpResponse("Hello, world. You're at the Intake landing page.")
