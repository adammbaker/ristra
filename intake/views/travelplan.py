from intake.choices import TRAVEL_MODE_CHOICES
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from intake.choices import TRAVEL_MODE_CHOICES
from intake.forms.sponsor import SponsorForm
from intake.forms.travelplan import AirlineTravelPlanForm, BusTravelPlanForm, TravelPlanForm
from intake.models import HeadOfHousehold, TravelPlan
from intake.utilities import category_from_choices

from datetime import datetime
# Create your views here.
class TravelPlanListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = TravelPlan
    paginate_by = 0

    def get_queryset(self):
        return HeadOfHousehold.objects.get(id=self.kwargs.get('id')).travelplan

class TravelPlanCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = TravelPlan
    parent = HeadOfHousehold
    form_class = TravelPlanForm
    template_name = 'intake/generic-form.html'

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Add %(model)s' % {
            'model': self.model.__name__
        }
        kwargs['title'] = 'Add a%(article_n)s %(model)s to %(target)s' % {
            'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
            'model': self.model.__name__,
            'target': self.parent.__name__
        }
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # tp_arranged_by = form.cleaned_data.get('arranged_by')
        tp_arranged_by = self.request.user.profile
        tp_confirmation = form.cleaned_data.get('confirmation')
        tp_destination_city = form.cleaned_data.get('destination_city')
        tp_destination_state = form.cleaned_data.get('destination_state')
        tp_travel_date = form.cleaned_data.get('travel_date')
        tp_city_van_date = form.cleaned_data.get('city_van_date')
        tp_travel_food_prepared = form.cleaned_data.get('travel_food_prepared')
        tp_eta = form.cleaned_data.get('eta')
        tp_travel_mode = form.cleaned_data.get('travel_mode')
        tp_notes = form.cleaned_data.get('notes')
        hoh = get_object_or_404(HeadOfHousehold, id=self.kwargs.get('hoh_id'))
        tp, tp_c = TravelPlan.objects.get_or_create(
            arranged_by = tp_arranged_by,
            confirmation = tp_confirmation,
            destination_city = tp_destination_city,
            destination_state = tp_destination_state,
            travel_date = tp_travel_date,
            city_van_date = tp_city_van_date,
            travel_food_prepared = tp_travel_food_prepared,
            eta = tp_eta,
            travel_mode = tp_travel_mode,
            notes = tp_notes,
        )
        # print('HOH',hoh.id, hoh.name)
        # print('TPP', tp, tp.id, tp_c)
        hoh.travel_plan = tp
        hoh.save()
        # Set appropriate travel mode
        travel_mode_category = category_from_choices(TRAVEL_MODE_CHOICES, tp.travel_mode)
        print('TP_c', travel_mode_category)
        if travel_mode_category not in ('Air','Bus'):
            # return to parent overview
            print('Sending to faimly overview for', hoh.id)
            return redirect('headofhousehold:overview', hoh_id = hoh.id)
        # if travel_mode_category == 'Air':
        #     self.request.session['travel_mode'] = 'Air'
        # elif travel_mode_category == 'Bus':
        #     self.request.session['travel_mode'] = 'Bus'
        # else:
        #     # return to parent detail
        #     print('Sending to faimly detail for', hoh.id)
        #     return redirect('headofhousehold:detail', hoh_id = hoh.id)
        self.request.session['travel_mode_category'] = travel_mode_category
        return redirect('travelplan:travel follow up', tp_id = tp.id)


class TravelPlanDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = TravelPlan

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['tp_id'])

class TravelPlanEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = TravelPlan
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['tp_id'])


class TravelModeFollowUpTemplateView(LoginRequiredMixin, TemplateView):
    airline_form_class = AirlineTravelPlanForm
    busline_form_class = BusTravelPlanForm
    template_name = 'intake/travel-mode-follow-up.html'

    def get_context_data(self, **kwargs):
        context = super(TravelModeFollowUpTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Follow Up Travel Questions'
        context['travel_plan'] = self.kwargs.get('tp_id')
        context['airline_form_class'] = self.airline_form_class
        context['busline_form_class'] = self.busline_form_class
        return context

    def get_success_url(self):
        tp_id = self.kwargs.get('tp_id')
        hoh_id = TravelPlan.objects.get(id=tp_id).headofhousehold
        return redirect('headofhousehold:detail', hoh_id = hoh_id)

    def form_valid(self, airline_form_class, busline_form_class):
        tp_id = self.kwargs.get('tp_id')
        tp = TravelPlan.objects.get(id=tp_id)
        travel_mode_category = category_from_choices(TRAVEL_MODE_CHOICES, tp.travel_mode)
        print('FV', travel_mode_category)
        if travel_mode_category == 'Air':
            tp.layovers = airline_form_class.cleaned_data.get('layovers')
        elif travel_mode_category == 'Bus':
            tp.layovers = airline_form_class.cleaned_data.get('layovers')
        tp.flight_number = airline_form_class.cleaned_data.get('flight_number')
        tp.save()
        return redirect('headofhousehold:detail', hoh_id = tp.householdhead.id)

    def post(self, request, *args, **kwargs):
        airline_form = self.airline_form_class(request.POST)
        busline_form = self.busline_form_class(request.POST)
        tp_id = self.kwargs.get('tp_id')
        tp = TravelPlan.objects.get(id=tp_id)
        if airline_form.is_valid():
            tp.layovers = airline_form.cleaned_data.get('layovers')
            tp.flight_number = airline_form.cleaned_data.get('flight_number')
        if busline_form.is_valid():
            tp.layovers = busline_form.cleaned_data.get('layovers')
        tp.save()
        return redirect('headofhousehold:detail', hoh_id = tp.headofhousehold.id)


class TravelPlanUpdate(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit/update the instance of an object'
    model = TravelPlan
    parent = HeadOfHousehold
    # fields = ('confirmation','destination_city','destination_state','travel_date','city_van_date','travel_food_prepared','eta','travel_mode','layovers','notes','flight_number',)
    form_class = TravelPlanForm
    pk_url_kwarg = 'tp_id'
    template_name = 'intake/generic-form.html'

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Update %(model)s' % {
            'model': self.model.__name__
        }
        kwargs['title'] = 'Edit a%(article_n)s %(model)s to %(target)s' % {
            'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
            'model': self.model.__name__,
            'target': self.parent.__name__
        }
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        # TK get logging in here for user
        return reverse_lazy('travelplan:detail', kwargs={'tp_id': self.kwargs.get('tp_id')})


class TravelPlanDelete(LoginRequiredMixin, DeleteView):
    model = TravelPlan
    pk_url_kwarg = 'tp_id'
    template_name = 'intake/confirm_delete.html'

    def get_success_url(self):
        # TK get logging in here for user
        hoh_id = self.model.objects.get(id=self.kwargs.get('tp_id')).householdhead.id
        return reverse_lazy('headofhousehold:overview', kwargs={'hoh_id': hoh_id})
