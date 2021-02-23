from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from intake.forms.asylee import AsyleeForm, AsyleeHealthFollowUpForm, AsyleeVaccineForm, AsyleeSickForm
from intake.models import Asylee, HeadOfHousehold

# Create your views here.
class AsyleeListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = Asylee
    paginate_by = 0

    def get_queryset(self):
        return self.request.user.locations()

class AsyleeCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Asylee
    parent = HeadOfHousehold
    form_class = AsyleeForm
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
        asylee_name = form.cleaned_data.get('name')
        asylee_sex = form.cleaned_data.get('sex')
        asylee_date_of_birth = form.cleaned_data.get('date_of_birth')
        asylee_phone_number = form.cleaned_data.get('phone_number')
        asylee_had_covid_disease = form.cleaned_data.get('had_covid_disease')
        asylee_had_covid_vaccine = form.cleaned_data.get('had_covid_vaccine')
        asylee_tsa_done = form.cleaned_data.get('tsa_done')
        asylee_legal_done = form.cleaned_data.get('legal_done')
        asylee_notes = form.cleaned_data.get('notes')
        hoh = get_object_or_404(HeadOfHousehold, id=self.kwargs.get('hoh_id'))
        asylee, asylee_c = Asylee.objects.get_or_create(
            name = asylee_name,
            sex = asylee_sex,
            date_of_birth = asylee_date_of_birth,
            phone_number = asylee_phone_number,
            had_covid_disease = asylee_had_covid_disease,
            had_covid_vaccine = asylee_had_covid_vaccine,
            tsa_done = asylee_tsa_done,
            legal_done = asylee_legal_done,
            notes = asylee_notes,
        )
        hoh.asylees.add(asylee)
        hoh.save()
        # if Asylee is currently sick or has received a COVID vaccine
        # send to a different form to capture this info
        print(form.cleaned_data.get('had_covid_vaccine'), type(form.cleaned_data.get('had_covid_vaccine')))
        print(form.cleaned_data.get('is_currently_sick'), type(form.cleaned_data.get('is_currently_sick')))
        if form.cleaned_data.get('had_covid_vaccine') == True or form.cleaned_data.get('is_currently_sick') == True:
            # return super().form_valid(form)
            self.request.session['had_covid_vaccine'] = form.cleaned_data.get('had_covid_vaccine')
            self.request.session['is_currently_sick'] = form.cleaned_data.get('is_currently_sick')
            return redirect('asylee:health follow up', asy_id = asylee.id)
        if form.cleaned_data.get('had_covid_vaccine') == True and form.cleaned_data.get('is_currently_sick') == True:
            return redirect('asylee:health follow up', asy_id = asylee.id)
        elif form.cleaned_data.get('had_covid_vaccine') == True:
            return redirect('asylee:health vaccine', asy_id = asylee.id)
        elif form.cleaned_data.get('is_currently_sick') == True:
            return redirect('asylee:health sick', asy_id = asylee.id)
        # return to parent detail
        print('Sending to faimly detail for', hoh.id)
        return redirect('headofhousehold:detail', hoh_id = hoh.id)

class AsyleeDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Asylee
    print('\n\nTRIP\n\n')

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs.get('asy_id'))

class AsyleeEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = Asylee
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs.get('asy_id'))

# class AsyleeHealthFormView(LoginRequiredMixin, FormView):
#     'Creates a new instance of the object and relates it to their parent'
#     model = Asylee
#     parent = HeadOfHousehold
#     form_class = AsyleeForm
#     template_name = 'intake/generic-form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['button_text'] = 'Add %(model)s' % {
#             'model': self.model.__name__
#         }
#         kwargs['title'] = 'Add a%(article_n)s %(model)s to %(target)s' % {
#             'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
#             'model': self.model.__name__,
#             'target': self.parent.__name__
#         }
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         asylee_name = form.cleaned_data.get('name')
#         asylee_sex = form.cleaned_data.get('sex')
#         asylee_date_of_birth = form.cleaned_data.get('date_of_birth')
#         asylee_phone_number = form.cleaned_data.get('phone_number')
#         asylee_tsa_done = form.cleaned_data.get('tsa_done')
#         asylee_legal_done = form.cleaned_data.get('legal_done')
#         asylee_notes = form.cleaned_data.get('notes')
#         hoh = get_object_or_404(HeadOfHousehold, id=self.kwargs.get('hoh_id'))
#         asylee, asylee_c = Asylee.objects.get_or_create(
#             name = asylee_name,
#             sex = asylee_sex,
#             date_of_birth = asylee_date_of_birth,
#             phone_number = asylee_phone_number,
#             tsa_done = asylee_tsa_done,
#             legal_done = asylee_legal_done,
#             notes = asylee_notes,
#         )
#         hoh.asylees.add(asylee)
#         hoh.save()
#         # if Asylee is currently sick or has received a COVID vaccine
#         # send to a different form to capture this info
#         print(form.cleaned_data.get('had_covid_vaccine'), type(form.cleaned_data.get('had_covid_vaccine')))
#         print(form.cleaned_data.get('is_currently_sick'), type(form.cleaned_data.get('is_currently_sick')))
#         if form.cleaned_data.get('had_covid_vaccine') == True or form.cleaned_data.get('is_currently_sick') == True:
#             return redirect('asylee:health follow up', asylee_id = asylee.id)
#         # return to parent detail
#         print('Sending to faimly detail for', hoh.id)
#         return redirect('headofhousehold:detail', hoh_id = hoh.id)

# class AsyleeHealthFollowUpFormView(LoginRequiredMixin, FormView):
#     template_name = 'intake/generic-form.html'
#     form_class = AsyleeHealthFollowUpForm

#     def get_success_url(self):
#         asylee_id = self.kwargs.get('asy_id')
#         hoh_id = Asylee.objects.get(id=asylee_id).householdhead
#         return reverse('headofhousehold:detail', hoh_id = hoh_id)

#     def get_context_data(self, **kwargs):
#         kwargs = super(AsyleeHealthFollowUpFormView, self).get_form_kwargs()
#         kwargs['button_text'] = 'Submit'
#         kwargs['title'] = 'Asylee Health Questionnaire'
#         return super().get_context_data(**kwargs)

#     def get_initial(self):
#         # Get the initial dictionary from the superclass method
#         initial = super(self.__class__, self).get_initial()
#         # Copy the dictionary so we don't accidentally change a mutable dict
#         initial = initial.copy()
#         # initial['name'] = self.request.user.profile.name
#         # initial['phone_number'] = self.request.user.profile.phone_number
#         # initial['languages'] = self.request.user.profile.languages.all()
#         # initial['capacities'] = self.request.user.profile.capacities.all()
#         # initial['role'] = self.request.user.profile.role
#         return initial

#     def form_valid(self, form):
#         # up_name = form.cleaned_data.get('name')
#         asy_id = self.kwargs.get('asy_id')
#         asylee = Asylee.objects.get(id=asy_id)
#         asy_covid_vaccine_shots = form.cleaned_data.get('covid_vaccine_shots')
#         asy_vaccine_received = form.cleaned_data.get('vaccine_received')
#         asy_sick_covid = form.cleaned_data.get('sick_covid')
#         asy_sick_other = form.cleaned_data.get('sick_other')
#         asylee.covid_vaccine_shots = asy_covid_vaccine_shots
#         asylee.vaccine_received = asy_vaccine_received
#         asylee.sick_covid = asy_sick_covid
#         asylee.sick_other = asy_sick_other
#         asylee.save()
#         return redirect('headofhousehold:detail', hoh_id = asylee.householdhead)

class AsyleeHealthFollowUpTemplateView(LoginRequiredMixin, TemplateView):
    vaccine_form_class = AsyleeVaccineForm
    sick_form_class = AsyleeSickForm
    template_name = 'intake/health-follow-up.html'

    def get_context_data(self, **kwargs):
        context = super(AsyleeHealthFollowUpTemplateView, self).get_context_data(**kwargs)
        context['asylee'] = self.kwargs.get('asy_id')
        context['vaccine_form_class'] = self.vaccine_form_class
        context['sick_form_class'] = self.sick_form_class
        return context

    def get_success_url(self):
        asylee_id = self.kwargs.get('asy_id')
        hoh_id = Asylee.objects.get(id=asylee_id).householdhead
        return redirect('headofhousehold:detail', hoh_id = hoh_id)

    def form_valid(self, vaccine_form_class, sick_form_class):
        asy_id = self.kwargs.get('asy_id')
        asylee = Asylee.objects.get(id=asy_id)
        asylee.covid_vaccine_shots = vaccine_form_class.cleaned_data.get('covid_vaccine_shots',0)
        asylee.vaccine_received = vaccine_form_class.cleaned_data.get('vaccine_received')
        asylee.sick_covid = sick_form_class.cleaned_data.get('sick_covid', False)
        asylee.sick_other = sick_form_class.cleaned_data.get('sick_other', False)
        asylee.save()
        return redirect('headofhousehold:detail', hoh_id = asylee.householdhead.id)

    def post(self, request, *args, **kwargs):
        vaccine_form = self.vaccine_form_class(request.POST)
        sick_form = self.sick_form_class(request.POST)
        asy_id = self.kwargs.get('asy_id')
        asylee = Asylee.objects.get(id=asy_id)
        if vaccine_form.is_valid():
            asylee.covid_vaccine_shots = vaccine_form.cleaned_data.get('covid_vaccine_shots',0)
            asylee.vaccine_received = vaccine_form.cleaned_data.get('vaccine_received')
        if sick_form.is_valid():
            asylee.sick_covid = sick_form.cleaned_data.get('sick_covid', False)
            asylee.sick_other = sick_form.cleaned_data.get('sick_other', False)
        asylee.save()
        return redirect('headofhousehold:detail', hoh_id = asylee.householdhead.id)
        # return render(request, self.template_name, {'vaccine_form_class': vaccine_form_class, 'sick_form_class': sick_form_class})
        # return render(request, self.template_name, {'form': form, 'profile_form': profile_form})