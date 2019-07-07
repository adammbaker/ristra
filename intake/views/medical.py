from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from intake.forms.medical import MedicalForm
from intake.models import Asylee, Family, Medical

# Create your views here.
@method_decorator([login_required], name='dispatch')
class MedicalCreationView(LoginRequiredMixin, CreateView):
    model = Medical
    form_class = MedicalForm
    template_name = 'intake/medical-add-form.html'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        initial['resolved'] = True
        return initial

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Medical Issue'
        kwargs['asylee'] = Asylee.objects.get(id=self.kwargs['asylee_id'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        med_provider = form.cleaned_data['provider']
        med_description = form.cleaned_data['description']
        med_notes = form.cleaned_data['notes']
        med_resolved = form.cleaned_data['resolved']
        asylee = get_object_or_404(Asylee, id=self.kwargs['asylee_id'])
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
        return redirect('asylee:detail', asylee_id = asylee.id)

class MedicalDetailView(LoginRequiredMixin, ListView):
    'Shows the current Medical'
    model = Medical
    context_object_name = 'med'
    ordering = ('-id', )
    paginate_by = 0
    template_name = 'intake/medical-detail.html'

    def get_queryset(self):
        queryset = get_object_or_404(self.model, id=self.kwargs['med_id'])
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(self.__class__, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['active_view'] = self.context_object_name
        return context
