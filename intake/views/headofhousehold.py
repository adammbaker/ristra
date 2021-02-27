from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView
# from intake.decorators import is_affiliated
from intake.forms.asylee import AsyleeForm, AsyleeVaccineForm, AsyleeSickForm
from intake.forms.headofhousehold import HeadOfHouseholdForm
from intake.models import Asylee, HeadOfHousehold, IntakeBus

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
        hoh_country_of_origin = form.cleaned_data.get('country_of_origin')
        hoh_notes = form.cleaned_data.get('notes')
        ib = get_object_or_404(IntakeBus, id=self.kwargs.get('ib_id'))
        hoh, hoh_c = HeadOfHousehold.objects.get_or_create(
            name = hoh_name,
            sex = hoh_sex,
            date_of_birth = hoh_date_of_birth,
            phone_number = hoh_phone_number,
            notes = hoh_notes,
            lodging = hoh_lodging,
            destination_city = hoh_destination_city,
            state = hoh_state,
            days_traveling = hoh_days_traveling,
            days_detained = hoh_days_detained,
            country_of_origin = hoh_country_of_origin,
        )
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
        if form.cleaned_data.get('had_covid_vaccine') == True or form.cleaned_data.get('is_currently_sick') == True:
            # return super().form_valid(form)
            self.request.session['had_covid_vaccine'] = form.cleaned_data.get('had_covid_vaccine')
            self.request.session['is_currently_sick'] = form.cleaned_data.get('is_currently_sick')
            return redirect('headofhousehold:health follow up', hoh_id = hoh.id)
        # return to parent detail
        return redirect('headofhousehold:detail', hoh_id = hoh.id)

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
        return redirect('headofhousehold:detail', hoh_id = hoh_id)

    def form_valid(self, vaccine_form_class, sick_form_class):
        hoh_id = self.kwargs.get('hoh_id')
        hoh = HeadOfHousehold.objects.get(id=hoh_id)
        hoh.covid_vaccine_shots = vaccine_form_class.cleaned_data.get('covid_vaccine_shots',0)
        hoh.vaccine_received = vaccine_form_class.cleaned_data.get('vaccine_received')
        hoh.sick_covid = sick_form_class.cleaned_data.get('sick_covid', False)
        hoh.sick_other = sick_form_class.cleaned_data.get('sick_other', False)
        hoh.save()
        return redirect('headofhousehold:detail', hoh_id = hoh.id)

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
        return redirect('headofhousehold:detail', hoh_id = hoh.id)



class HeadOfHouseholdOverview(LoginRequiredMixin, DetailView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'
    template_name = 'intake/headofhousehold_overview.html'

    def get_context_data(self, **kwargs):
        kwargs['lod'] = 'partial'
        return super().get_context_data(**kwargs)


class HeadOfHouseholdDetail(LoginRequiredMixin, DetailView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'


class HeadOfHouseholdList(LoginRequiredMixin, ListView):
    model = HeadOfHousehold
    pk_url_kwarg = 'hoh_id'
