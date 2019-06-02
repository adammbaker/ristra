from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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

def index(request):
    return HttpResponse("Hello, world. You're at the Intake landing page.")

class HomePageView(TemplateView):
    template_name = "intake/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context

def login(request):
    return HttpResponse("Hello, world. You're at the Intake login page.")


class LoginPageView(TemplateView):
    template_name = "intake/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        messages.info(self.request, "hello login")
        return context

@login_required
def landing_page(request):
    'Determine the appropriate landing page for the user'
    resp = []
    resp.append('There are %d locations.' % Locations.objects.count())
    resp.append('There are %d buses.' % IntakeBuses.objects.count())
    resp.append('There are %d families.' % Families.objects.count())
    return HttpResponse('<p>'.join(resp))
    if not Families.objects.exists():
        return HttpResponseRedirect(reverse('intake buses landing page'))
    if not IntakeBuses.objects.exists():
        return HttpResponseRedirect(reverse('location landing page'))
    if not Location.objects.exists():
        return HttpResponseRedirect(reverse('location add page'))

# def locations(request):
#     'Show locations, or send to Location Add form page if none'
#     if not Families.objects.exists():
#         return HttpResponseRedirect(reverse('home'))

# def intake_buses(request):
#     'Show intake buses, or send to Location landing page if none'
#     if request.method =='POST':
#         form = intakebuses.IntakeBusForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('home')
#     else:
#         form = intakebuses.IntakeBusForm()
#     return render(request, 'intake/intakebus-add.html', {'form': form})

# @login_required
# def family(request):
#     'Show families, or send to Buses landing page if no families'
#     if request.method =='POST':
#         form = FamilyForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('home')
#     else:
#         form = FamilyForm()
#     return render(request, 'intake/family-add.html', {'form': form})
#
# class FamilyAddPageView(LoginRequiredMixin, TemplateView):
#     template_name = "intake/family-add.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(FamilyAddPageView, self).get_context_data(**kwargs)
#         context['form'] = FamilyForm()
#         messages.info(self.request, "hello fam")
#         return context
