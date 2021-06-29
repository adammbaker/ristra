from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# from intake.decorators import is_affiliated
from intake.forms.asylee import AsyleeForm, AsyleeVaccineForm, AsyleeSickForm
from intake.forms.headofhousehold import HeadOfHouseholdForm
from intake.models import Asylee, HeadOfHousehold, HouseholdNeed, IntakeBus

# Create your views here.
class HeadOfHouseholdListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = HeadOfHousehold
    paginate_by = 0

    def get_queryset(self):
        return self.request.user.locations()

class HeadOfHouseholdCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = HeadOfHousehold
    parent = IntakeBus
    form_class = HeadOfHouseholdForm
    template_name = 'intake/generic-form.html'

    # def get_form_kwargs(self):
    #     kwargs = {'vol_avail' : IntakeBus.objects.get(id=self.kwargs.get('ib_id')).location_set.first().organization_set.first().campaign_set.first().user_set.all() , }
    #     return kwargs

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Add %(model)s' % {
            'model': self.model.__name__
        }
        kwargs['title'] = 'Add a%(article_n)s %(model)s to %(target)s' % {
            'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
            'model': self.model.__name__,
            'target': self.parent.__name__
        }
        # kwargs['vol_avail'] = IntakeBus.objects.get(id=self.kwargs.get('ib_id')).location_set.first().organization_set.first().campaign_set.first().user_set.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        hoh_intake_by = self.request.user
        hoh_name = form.cleaned_data.get('name')
        hoh_a_number = form.cleaned_data.get('a_number')
        hoh_sex = form.cleaned_data.get('sex')
        hoh_date_of_birth = form.cleaned_data.get('date_of_birth')
        hoh_phone_number = form.cleaned_data.get('phone_number')
        hoh_notes = form.cleaned_data.get('notes')
        hoh_lodging = form.cleaned_data.get('lodging')
        hoh_destination_city = form.cleaned_data.get('destination_city')
        hoh_state = form.cleaned_data.get('state')
        hoh_languages = form.cleaned_data.get('languages')
        hoh_days_traveling = form.cleaned_data.get('days_traveling')
        hoh_days_detained = form.cleaned_data.get('days_detained')
        hoh_detention_type = form.cleaned_data.get('detention_type')
        hoh_country_of_origin = form.cleaned_data.get('country_of_origin')
        hoh_notes = form.cleaned_data.get('notes')
        ib = get_object_or_404(IntakeBus, id=self.kwargs.get('ib_id'))
        hoh, hoh_c = HeadOfHousehold.objects.get_or_create(
            name = hoh_name,
            sex = hoh_sex,
            date_of_birth = hoh_date_of_birth,
        )
        hoh.a_number = hoh_a_number
        hoh.phone_number = hoh_phone_number
        hoh.notes = hoh_notes
        hoh.lodging = hoh_lodging
        hoh.destination_city = hoh_destination_city
        hoh.state = hoh_state
        hoh.days_traveling = hoh_days_traveling
        hoh.days_detained = hoh_days_detained
        hoh.detention_type = hoh_detention_type
        hoh.country_of_origin = hoh_country_of_origin
        hoh.languages.set(hoh_languages)
        hoh.intake_by = hoh_intake_by.profile
        hoh.notes = hoh_notes
        asy = Asylee.objects.get(
            name = hoh_name,
            sex = hoh_sex,
            date_of_birth = hoh_date_of_birth,
        )
        hoh.asylees.add(asy)
        ib.headsofhousehold.add(hoh)
        ib.save()
        hoh.save()
        # Historical data
        if form.cleaned_data.get('had_covid_vaccine') == True or form.cleaned_data.get('is_currently_sick') == True:
            # return super().form_valid(form)
            self.request.session['had_covid_vaccine'] = form.cleaned_data.get('had_covid_vaccine')
            self.request.session['is_currently_sick'] = form.cleaned_data.get('is_currently_sick')
            return reverse_lazy('headofhousehold:health follow up', hoh_id = hoh.id)
        # return to parent detail
        UpdateHistorical(hoh)
        return reverse_lazy('headofhousehold:overview', hoh_id = hoh.id)

# @method_decorator([is_affiliated], name='dispatch')
class HeadOfHouseholdDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = HeadOfHousehold

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['hoh_id'])

class HeadOfHouseholdEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = HeadOfHousehold
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['hoh_id'])

class HeadOfHouseholdHealthFollowUpTemplateView(LoginRequiredMixin, TemplateView):
    vaccine_form_class = AsyleeVaccineForm
    sick_form_class = AsyleeSickForm
    template_name = 'intake/health-follow-up.html'

    def get_context_data(self, **kwargs):
        context = super(HeadOfHouseholdHealthFollowUpTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Follow Up Health Questions'
        context['asylee'] = self.kwargs.get('hoh_id')
        context['vaccine_form_class'] = self.vaccine_form_class 
        context['sick_form_class'] = self.sick_form_class
        return context

    def get_success_url(self):
        hoh_id = self.kwargs.get('hoh_id')
        hoh_id = HeadOfHousehold.objects.get(id=hoh_id).householdhead
        return reverse_lazy('headofhousehold:overview', hoh_id = hoh_id)

    def form_valid(self, vaccine_form_class, sick_form_class):
        hoh_id = self.kwargs.get('hoh_id')
        hoh = HeadOfHousehold.objects.get(id=hoh_id)
        hoh.covid_vaccine_shots = vaccine_form_class.cleaned_data.get('covid_vaccine_shots',0)
        hoh.vaccine_received = vaccine_form_class.cleaned_data.get('vaccine_received')
        hoh.sick_covid = sick_form_class.cleaned_data.get('sick_covid', False)
        hoh.sick_other = sick_form_class.cleaned_data.get('sick_other', False)
        hoh.save()
        UpdateHistorical(hoh)
        return reverse_lazy('headofhousehold:overview', hoh_id = hoh.id)

    def post(self, request, *args, **kwargs):
        vaccine_form = self.vaccine_form_class(request.POST)
        sick_form = self.sick_form_class(request.POST)
        hoh_id = self.kwargs.get('hoh_id')
        hoh = HeadOfHousehold.objects.get(id=hoh_id)
        if vaccine_form.is_valid():
            hoh.covid_vaccine_shots = vaccine_form.cleaned_data.get('covid_vaccine_shots',0)
            hoh.vaccine_received = vaccine_form.cleaned_data.get('vaccine_received')
        if sick_form.is_valid():
            hoh.sick_covid = sick_form.cleaned_data.get('sick_covid', False)
            hoh.sick_other = sick_form.cleaned_data.get('sick_other', False)
        hoh.save()
        return reverse_lazy('headofhousehold:overview', hoh_id = hoh.id)



class HeadOfHouseholdOverview(LoginRequiredMixin, DetailView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'
    template_name = 'intake/headofhousehold_overview.html'

    def get_context_data(self, **kwargs):
        kwargs['householdneeds'] = HouseholdNeed.objects.all()
        kwargs['lod'] = 'partial'
        return super().get_context_data(**kwargs)


class HeadOfHouseholdDetail(LoginRequiredMixin, DetailView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'


class HeadOfHouseholdList(LoginRequiredMixin, ListView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'


class HeadOfHouseholdUpdate(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit/update the instance of an object'
    model = HeadOfHousehold
    parent = IntakeBus
    fields = ('languages','lodging','destination_city','state','days_traveling','days_detained','country_of_origin','name','a_number','sex','date_of_birth','phone_number','had_covid_disease','had_covid_vaccine','covid_vaccine_doses','vaccine_received','sick_covid','sick_other','notes',)
    # form_class = HeadOfHouseholdForm
    pk_url_kwarg = 'hoh_id'
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
        return reverse_lazy('headofhousehold:detail', kwargs={'hoh_id': self.kwargs.get('hoh_id')})


class HeadOfHouseholdDelete(LoginRequiredMixin, DeleteView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'
    template_name = 'intake/confirm_delete.html'

    def get_success_url(self):
        # TK get logging in here for user
        ib_id = self.model.objects.get(id=self.kwargs.get('hoh_id')).intakebus.id
        return reverse_lazy('intakebus:overview', kwargs={'ib_id': ib_id})


class ItineraryDetail(LoginRequiredMixin, DetailView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'
    template_name = 'intake/itinerary.html'


@login_required
def AddNeedToHousehold(request, hoh_id, need_id):
    if request.user.profile.is_capable_travel or request.user.profile.is_capable_intake:
        need = HouseholdNeed.objects.get(id=need_id)
        hoh = HeadOfHousehold.objects.get(id=hoh_id)
        hoh.needs.add(need)
        hoh.save()
        messages.success(request, f'{need} was successfully added for {hoh}')
        org = hoh.intakebus.location.organization
        if need.need in org.historical_needs.keys():
            org.historical_needs[need.need] += 1
        else:
            org.historical_needs[need.need] = 1
        org.save()
    else:
        messages.error(request, "Unable to add that need to that household.")
    print('F')
    return reverse_lazy('headofhousehold:overview', hoh_id=hoh_id)


@login_required
def SatisfyNeedForHousehold(request, hoh_id, need_id):
    if request.user.profile.is_capable_travel or request.user.profile.is_capable_intake or request.user.profile.is_capable_concierge:
        need = HouseholdNeed.objects.get(id=need_id)
        hoh = HeadOfHousehold.objects.get(id=hoh_id)
        hoh.needs.remove(need)
        hoh.save()
        messages.success(request, f'{need} was satisfied for {hoh}')
    else:
        messages.error(request, "Unable to satisfy that need to that household.")
    print('F')
    return reverse_lazy('headofhousehold:overview', hoh_id=hoh_id)


def UpdateHistorical(hoh):
    'Updates historical data for the organization'
    org = hoh.intakebus.location.organization
    org.historical_families_count += 1
    if hoh.sex in org.historical_sex_count.keys():
        org.historical_sex_count[hoh.sex] += 1
    else:
        org.historical_sex_count[hoh.sex] = 1
    if hoh.age in org.historical_age_count.keys():
        org.historical_age_count[hoh.age] += 1
    else:
        org.historical_age_count[hoh.age] = 1
    if hoh.country_of_origin in org.historical_country_of_origin.keys():
        org.historical_country_of_origin[hoh.country_of_origin] += 1
    else:
        org.historical_country_of_origin[hoh.country_of_origin] = 1
    org.historical_days_traveling += hoh.days_traveling
    org.historical_days_in_detention += hoh.days_detained
    if hoh.detention_type in org.historical_detention_type.keys():
        org.historical_detention_type[hoh.detention_type] += 1
    else:
        org.historical_detention_type[hoh.detention_type] = 1
    if hoh.destination in org.historical_destinations.keys():
        org.historical_destinations[hoh.destination] += 1
    else:
        org.historical_destinations[hoh.destination] = 1
    languages = ', '.join(list(hoh.languages.values_list('language',flat=True)))
    if languages in org.historical_languages_spoken.keys():
        org.historical_languages_spoken[languages] += 1
    else:
        org.historical_languages_spoken[languages] = 1
    # Asylee specific stuff but still associated with HoH
    org.historical_asylees_count += 1
    if hoh.sex in org.historical_sex_count.keys():
        org.historical_sex_count[hoh.sex] += 1
    else:
        org.historical_sex_count[hoh.sex] = 1
    if hoh.age in org.historical_age_count.keys():
        org.historical_age_count[hoh.age] += 1
    else:
        org.historical_age_count[hoh.age] = 1
    for asy in hoh.asylees.all():
        if asy.sick_covid:
            org.historical_sick_covid += 1
        if asy.sick_other:
            org.historical_sick_other += 1
    org.save()