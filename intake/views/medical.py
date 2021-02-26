from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
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
        # return to parent detail
        print('Sending to asylee detail for', asylee.id)
        return redirect('asylee:detail', asy_id = asylee.id)

class MedicalDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Medical

    def get_object(self, **kwargs):
        medical_capacity = Capacity.objects.get(name='Medical')
        medical_in_user_capacities = medical_capacity in self.request.user.profile.capacities.all()
        if self.request.user.profile.is_capable_medical:
            return self.model.objects.get(id=self.kwargs['med_id'])
        messages.warning(self.request, ('You do not have appropriate access for this page'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

class MedicalEditView(LoginRequiredMixin, UpdateView):
    'Allows a privileged user to to edit the instance of an object'
    model = Medical
    template_name = 'intake/generic-form.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['med_id'])




# @method_decorator([login_required], name='dispatch')
# class MedicalCreationView(LoginRequiredMixin, CreateView):
#     model = Medical
#     form_class = MedicalForm
#     template_name = 'intake/medical-add-form.html'
#
#     def get_initial(self, *args, **kwargs):
#         initial = super(self.__class__, self).get_initial(**kwargs)
#         initial['resolved'] = True
#         return initial
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'Medical Issue'
#         kwargs['asylee'] = Asylee.objects.get(id=self.kwargs['asylee_id'])
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         med_provider = form.cleaned_data['provider']
#         med_description = form.cleaned_data['description']
#         med_notes = form.cleaned_data['notes']
#         med_resolved = form.cleaned_data['resolved']
#         asylee = get_object_or_404(Asylee, id=self.kwargs['asylee_id'])
#         med, med_c = Medical.objects.get_or_create(
#             provider = med_provider,
#             description = med_description,
#             notes = med_notes,
#         )
#         if med_resolved:
#             med.resolution_time = timezone.now()
#             med.save()
#         asylee.medicals.add(med)
#         asylee.save()
#         # return to parent detail
#         print('Sending to asylee detail for', asylee.id)
#         return redirect('asylee:detail', asylee_id = asylee.id)
#
# class MedicalDetailView(LoginRequiredMixin, ListView):
#     'Shows the current Medical'
#     model = Medical
#     context_object_name = 'med'
#     ordering = ('-id', )
#     paginate_by = 0
#     template_name = 'intake/medical-detail.html'
#
#     def get_queryset(self):
#         queryset = get_object_or_404(self.model, id=self.kwargs['med_id'])
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['active_view'] = self.context_object_name
#         return context
