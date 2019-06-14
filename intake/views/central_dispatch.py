from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.generic.base import TemplateView

# from intake.forms import family
# from intake.forms import forms, family, intakebuses
# from intake.forms.family import FamilyForm
from intake.models import *

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

def dispatch(request):
    'Determine the appropriate landing page for the user'
    if request.user.is_authenticated:
        # send user to page asking them to affiliate with an organization
        print('Active user sessions - 0')
        print('campaigns' in request.session.keys())
        print('REEFER', request.META.get('HTTP_REFERER'))
        # determine if user is a Point Of Contact or Deputy for an organization whose organization is not completely set up
        is_poc = Q(point_of_contact=request.user.volunteers)
        is_deputy = Q(deputies=request.user.volunteers)
        user_affiliations = Organizations.objects.filter(is_poc | is_deputy)
        if user_affiliations.exists():
            # check if user's organization information is missing any fields
            needs_name = Q(name=None)
            needs_city = Q(city=None)
            needs_state = Q(state=None)
            if user_affiliations.filter(needs_name | needs_city | needs_state).exists():
                return HttpResponse(reverse('org detail fill', kwargs={'id': user_affiliations.first().id}))
            # if POC/deputy's org is filled out, send to the organization admin page to add Locations or
            print('Active user sessions - 1')
            print('campaigns' in request.session.keys())
            return HttpResponseRedirect(reverse('org detail admin', kwargs={'id': user_affiliations.first().id}))
        # otherwise, check if the user has any active affiliations
        print('Active user sessions - 2')
        print('campaigns' in request.session.keys())
        return HttpResponseRedirect(reverse('families'))
    return HttpResponseRedirect(reverse('signup'))
