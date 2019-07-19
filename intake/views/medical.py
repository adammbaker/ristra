from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from intake.forms.medical import MedicalForm
from intake.models import Asylee, Family, Medical

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
        initial['resolved'] = True
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
        print('tEST')
        med_provider = form.cleaned_data.get('provider')
        med_description = form.cleaned_data.get('description')
        med_notes = form.cleaned_data.get('notes')
        med_resolved = form.cleaned_data.get('resolved')
        asylee = get_object_or_404(Asylee, id=self.kwargs.get('asy_id'))
        med, med_c = Medical.objects.get_or_create(
            provider = med_provider,
            description = med_description,
            notes = med_notes,
        )
        if med_resolved:
            med.resolution_time = timezone.now()
            med.save()
        asylee.medicals.add(med)
        asylee.save()
        # return to parent detail
        print('Sending to asylee detail for', asylee.id)
        return redirect('asylee:detail', asy_id = asylee.id)

class MedicalDetailView(LoginRequiredMixin, DetailView):
    'Details an instance of the object'
    model = Medical

    def get_object(self, **kwargs):
        return self.model.objects.get(id=self.kwargs['med_id'])

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
