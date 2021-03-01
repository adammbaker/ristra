from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from intake.forms.medical import MedicalForm
from intake.models import Asylee, Capacity, HeadOfHousehold, Medical, Profile

# Create your views here.
class MedicalListView(LoginRequiredMixin, ListView):
    'Lists all objects related to their parent'
    model = Medical
    paginate_by = 0

    def get_queryset(self):
        return Asylee.objects.get(id=self.kwargs.get('asy_id')).medical.all()

class MedicalCreateView(LoginRequiredMixin, CreateView):
    'Creates a new instance of the object and relates it to their parent'
    model = Medical
    parent = Asylee
    form_class = MedicalForm
    template_name = 'intake/generic-form.html'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        medical_capacity = Capacity.objects.filter(name='Medical')
        initial['provider'] = Profile.objects.filter(capacities__in=medical_capacity)
        return initial

    def get_context_data(self, **kwargs):
        kwargs['button_text'] = 'Add %(model)s' % {
            'model': self.model.__name__
        }
        kwargs['title'] = 'Add a%(article_n)s %(model)s to %(target)s' % {
            'article_n': 'n' if max([self.model.__name__.lower().startswith(x) for x in list('aeiou')]) else '',
            'model': self.model.__name__,
            'target': self.parent.__name__
        }
        kwargs[self.model.__name__.lower()] = self.model.objects.first()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        med_provider = form.cleaned_data.get('provider')
        med_entered_by = self.request.user.profile
        med_temperature = form.cleaned_data.get('temperature')
        med_pulse = form.cleaned_data.get('pulse')
        med_blood_pressure = form.cleaned_data.get('blood_pressure')
        med_weight = form.cleaned_data.get('weight')
        med_height = form.cleaned_data.get('height')
        med_oxgyen_level = form.cleaned_data.get('oxgyen_level')
        med_vaccines_received = form.cleaned_data.get('vaccines_received')
        med_allergies = form.cleaned_data.get('allergies')
        med_medications = form.cleaned_data.get('medications')
        med_chronic_medical_problems = form.cleaned_data.get('chronic_medical_problems')
        med_symptoms = form.cleaned_data.get('symptoms')
        med_diagnosis = form.cleaned_data.get('diagnosis')
        med_treatment = form.cleaned_data.get('treatment')
        med_follow_up_needed = form.cleaned_data.get('follow_up_needed')
        med_notes = form.cleaned_data.get('notes')
        asylee = get_object_or_404(Asylee, id=self.kwargs.get('asy_id'))
        med = Medical.objects.create(
            provider = med_provider,
            entered_by = med_entered_by,
            temperature = med_temperature,
            pulse = med_pulse,
            blood_pressure = med_blood_pressure,
            weight = med_weight,
            height = med_height,
            oxgyen_level = med_oxgyen_level,
            vaccines_received = med_vaccines_received,
            allergies = med_allergies,
            medications = med_medications,
            chronic_medical_problems = med_chronic_medical_problems,
            symptoms = med_symptoms,
            diagnosis = med_diagnosis,
            treatment = med_treatment,
            follow_up_needed = med_follow_up_needed,
            notes = med_notes,
        )
        asylee.medicals.add(med)
        asylee.save()
        # return to parent overview
        print('Sending to asylee overview for', asylee.id)
        return redirect('asylee:overview', asy_id = asylee.id)

class MedicalDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Medical

    def test_func(self):
        return self.request.user.profile.is_capable_medical

    def get_object(self, **kwargs):
        medical_capacity = Capacity.objects.get(name='Medical')
        medical_in_user_capacities = medical_capacity in self.request.user.profile.capacities.all()
        if self.request.user.profile.is_capable_medical:
            print('XX')
            return self.model.objects.get(id=self.kwargs['med_id'])
        asy_id = self.model.objects.get(id=self.kwargs['med_id']).asylee.id
        print('YY', asy_id)
        messages.warning(self.request, ('You do not have appropriate access for this page'))
        return reverse_lazy('asylee:overview', kwargs={'asy_id': asy_id})

class MedicalEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = Medical
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['med_id'])


class MedicalUpdate(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit/update the instance of an object'
    model = Medical
    parent = Asylee
    # fields = ('provider','temperature','pulse','blood_pressure','weight','height','oxgyen_level','vaccines_received','allergies','medications','chronic_medical_problems','symptoms','diagnosis','treatment','follow_up_needed','notes',)
    form_class = MedicalForm
    pk_url_kwarg = 'med_id'
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
        return reverse_lazy('medical:detail', kwargs={'med_id': self.kwargs.get('med_id')})


class MedicalDelete(LoginRequiredMixin, DeleteView):
    model = Medical
    pk_url_kwarg = 'med_id'
    template_name = 'intake/confirm_delete.html'

    def get_success_url(self):
        # TK get logging in here for user
        asy_id = self.model.objects.get(id=self.kwargs.get('med_id')).asylee.id
        return reverse_lazy('asylee:overview', kwargs={'asy_id': asy_id})
