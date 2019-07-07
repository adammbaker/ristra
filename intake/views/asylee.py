from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from intake.forms.asylee import AsyleeForm
from intake.models import Asylee, Family

# Create your views here.
@method_decorator([login_required], name='dispatch')
class AsyleeCreationView(LoginRequiredMixin, CreateView):
    model = Asylee
    form_class = AsyleeForm
    template_name = 'intake/asylee-add-form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Asylee'
        kwargs['family'] = Family.objects.get(id=self.kwargs['fam_id'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        asylee_name = form.cleaned_data['name']
        asylee_sex = form.cleaned_data['sex']
        asylee_date_of_birth = form.cleaned_data['date_of_birth']
        asylee_phone_number = form.cleaned_data['phone_number']
        asylee_tsa_done = form.cleaned_data['tsa_done']
        asylee_legal_done = form.cleaned_data['legal_done']
        asylee_notes = form.cleaned_data['notes']
        fam = get_object_or_404(Family, id=self.kwargs['fam_id'])
        asylee, asylee_c = Asylee.objects.get_or_create(
            name = asylee_name,
            sex = asylee_sex,
            date_of_birth = asylee_date_of_birth,
            phone_number = asylee_phone_number,
            tsa_done = asylee_tsa_done,
            legal_done = asylee_legal_done,
            notes = asylee_notes,
        )
        fam.asylees.add(asylee)
        fam.save()
        # return to parent detail
        print('Sending to faimly detail for', fam.id)
        return redirect('family:detail', fam_id = fam.id)

class AsyleeDetailView(LoginRequiredMixin, ListView):
    'Shows the current Asylee and its children'
    model = Asylee
    context_object_name = 'asylee'
    ordering = ('-id', )
    paginate_by = 0
    template_name = 'intake/asylee-detail.html'

    def get_queryset(self):
        queryset = get_object_or_404(self.model, id=self.kwargs['asylee_id'])
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(self.__class__, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['active_view'] = self.context_object_name
        return context
